// On-screen touch controls: left joystick = WASD, right side drag = look, buttons = keys.
// Feeds the existing Input class (keys / pressed / look) so no gameplay code has to change.
// Only active on touch devices (or with ?touch in the URL).
export function isTouchDevice() {

	return /[?&]touch\b/.test( location.search ) || ( 'ontouchstart' in window ) || navigator.maxTouchPoints > 0;

}

export class TouchControls {

	constructor( input ) {

		this.input = input;
		this.held = new Set();
		this.lookSens = 2.2; // multiplier on touch deltas (Player scales by 0.0022 rad/px)
		this._build();

	}

	_press( code ) {

		if ( ! this.input.keys.has( code ) ) this.input.pressed.add( code );
		this.input.keys.add( code );

	}

	_release( code ) {

		this.input.keys.delete( code );

	}

	_build() {

		const style = document.createElement( 'style' );
		style.textContent = `
			html, body, canvas { -webkit-touch-callout: none !important; -webkit-user-select: none !important; user-select: none !important; -webkit-tap-highlight-color: transparent; touch-action: none; }
			canvas { -webkit-user-drag: none; }
			.tt-layer { position: fixed; inset: 0; z-index: 50; pointer-events: none; touch-action: none; -webkit-user-select: none; user-select: none; -webkit-touch-callout: none; }
			.tt-look { position: absolute; top: 0; right: 0; width: 55%; height: 100%; pointer-events: auto; touch-action: none; }
			.tt-stick { position: absolute; left: max(28px, env(safe-area-inset-left)); bottom: max(28px, env(safe-area-inset-bottom)); width: 150px; height: 150px; border-radius: 50%; background: rgba(255,255,255,.12); border: 2px solid rgba(255,255,255,.35); pointer-events: auto; touch-action: none; }
			.tt-knob { position: absolute; left: 50%; top: 50%; width: 64px; height: 64px; margin: -32px 0 0 -32px; border-radius: 50%; background: rgba(255,255,255,.45); border: 2px solid rgba(255,255,255,.7); }
			.tt-btn { position: absolute; width: 58px; height: 58px; border-radius: 50%; background: rgba(20,30,45,.55); border: 2px solid rgba(255,255,255,.45); color: #fff; font: 600 13px -apple-system, system-ui, sans-serif; display: flex; align-items: center; justify-content: center; pointer-events: auto; touch-action: none; backdrop-filter: blur(6px); -webkit-backdrop-filter: blur(6px); }
			.tt-btn.on { background: rgba(80,160,255,.75); }
			.tt-btn.small { width: 44px; height: 44px; font-size: 11px; }
		`;
		document.head.appendChild( style );

		const layer = document.createElement( 'div' );
		layer.className = 'tt-layer';
		document.body.appendChild( layer );
		this.layer = layer;

		// ---- look pad (right side, under the buttons) ----
		const lookPad = document.createElement( 'div' );
		lookPad.className = 'tt-look';
		layer.appendChild( lookPad );
		let lookId = null, lx = 0, ly = 0;
		lookPad.addEventListener( 'pointerdown', ( e ) => {

			if ( lookId !== null ) return;
			lookId = e.pointerId; lx = e.clientX; ly = e.clientY;
			lookPad.setPointerCapture( e.pointerId );
			window.dispatchEvent( new Event( 'tt-activity' ) );

		} );
		lookPad.addEventListener( 'pointermove', ( e ) => {

			if ( e.pointerId !== lookId ) return;
			this.input.look.x += ( e.clientX - lx ) * this.lookSens;
			this.input.look.y += ( e.clientY - ly ) * this.lookSens;
			lx = e.clientX; ly = e.clientY;

		} );
		const endLook = ( e ) => { if ( e.pointerId === lookId ) lookId = null; };
		lookPad.addEventListener( 'pointerup', endLook );
		lookPad.addEventListener( 'pointercancel', endLook );

		// ---- joystick (left) ----
		const stick = document.createElement( 'div' );
		stick.className = 'tt-stick';
		const knob = document.createElement( 'div' );
		knob.className = 'tt-knob';
		stick.appendChild( knob );
		layer.appendChild( stick );
		let stickId = null;
		const R = 55, DEAD = 0.25;
		const setDir = ( nx, ny ) => {

			const want = { KeyW: ny < - DEAD, KeyS: ny > DEAD, KeyA: nx < - DEAD, KeyD: nx > DEAD };
			for ( const k in want ) want[ k ] ? this._press( k ) : this._release( k );
			// pushing the stick fully forward = sprint
			( ny < - 0.9 ) ? this._press( 'ShiftLeft' ) : ( this.sprintLatched || this._release( 'ShiftLeft' ) );

		};
		const moveStick = ( e ) => {

			const r = stick.getBoundingClientRect();
			let dx = e.clientX - ( r.left + r.width / 2 ), dy = e.clientY - ( r.top + r.height / 2 );
			const d = Math.hypot( dx, dy ) || 1;
			const c = Math.min( d, R );
			dx = dx / d * c; dy = dy / d * c;
			knob.style.transform = `translate(${ dx }px, ${ dy }px)`;
			setDir( dx / R, dy / R );

		};
		stick.addEventListener( 'pointerdown', ( e ) => {

			if ( stickId !== null ) return;
			stickId = e.pointerId;
			stick.setPointerCapture( e.pointerId );
			moveStick( e );

		} );
		stick.addEventListener( 'pointermove', ( e ) => { if ( e.pointerId === stickId ) moveStick( e ); } );
		const endStick = ( e ) => {

			if ( e.pointerId !== stickId ) return;
			stickId = null;
			knob.style.transform = '';
			setDir( 0, 0 );

		};
		stick.addEventListener( 'pointerup', endStick );
		stick.addEventListener( 'pointercancel', endStick );

		// ---- buttons (right, bottom) ----
		const mk = ( label, code, right, bottom, opts = {} ) => {

			const b = document.createElement( 'div' );
			b.className = 'tt-btn' + ( opts.small ? ' small' : '' );
			b.textContent = label;
			b.style.right = `calc(${ right }px + env(safe-area-inset-right))`;
			b.style.bottom = `calc(${ bottom }px + env(safe-area-inset-bottom))`;
			layer.appendChild( b );
			let id = null;
			b.addEventListener( 'pointerdown', ( e ) => {

				e.stopPropagation();
				if ( opts.toggle ) {

					const on = ! this.input.keys.has( code );
					on ? this._press( code ) : this._release( code );
					if ( code === 'ShiftLeft' ) this.sprintLatched = on;
					b.classList.toggle( 'on', on );
					return;

				}
				if ( opts.tap ) { this._press( code ); setTimeout( () => this._release( code ), 60 ); return; }
				id = e.pointerId; b.setPointerCapture( id ); this._press( code ); b.classList.add( 'on' );

			} );
			const up = ( e ) => { if ( id !== null && e.pointerId === id ) { id = null; this._release( code ); b.classList.remove( 'on' ); } };
			b.addEventListener( 'pointerup', up );
			b.addEventListener( 'pointercancel', up );
			return b;

		};

		mk( 'Jump', 'Space', 28, 110 );
		mk( 'Dive', 'KeyC', 98, 60 );
		mk( 'E', 'KeyE', 98, 130, { tap: true } );
		mk( 'Run', 'ShiftLeft', 28, 40, { toggle: true } );
		mk( 'Light', 'KeyL', 168, 40, { small: true, tap: true } );
		mk( 'Boat cam', 'KeyV', 168, 96, { small: true, tap: true } );
		mk( 'Free', 'KeyF', 168, 152, { small: true, tap: true } );
		mk( 'Menu', 'KeyH', 28, 190, { small: true, tap: true } );

		// keep the page from scrolling / zooming / pull-to-refresh under the game
		document.addEventListener( 'touchmove', ( e ) => e.preventDefault(), { passive: false } );
		document.addEventListener( 'gesturestart', ( e ) => e.preventDefault() );

	}

}
