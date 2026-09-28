#!/usr/bin/env python3
"""Generates ios/Tidewater.xcodeproj/project.pbxproj from scratch.

Run from the ios/ directory: `python3 generate_project.py`
Regenerate any time the file list changes instead of hand-editing the pbxproj.
"""
import os

# Fixed 24-hex-char IDs (pbxproj convention). Stable across regenerations.
IDS = {
    "app_swift_ref": "AA0000000000000000000001",
    "content_swift_ref": "AA0000000000000000000002",
    "infoplist_ref": "AA0000000000000000000003",
    "dist_ref": "AA0000000000000000000004",
    "product_ref": "AA0000000000000000000005",

    "app_swift_build": "BB0000000000000000000001",
    "content_swift_build": "BB0000000000000000000002",
    "dist_build": "BB0000000000000000000003",

    "root_group": "CC0000000000000000000001",
    "app_group": "CC0000000000000000000002",
    "products_group": "CC0000000000000000000003",

    "target": "DD0000000000000000000001",
    "project": "DD0000000000000000000002",

    "sources_phase": "EE0000000000000000000001",
    "resources_phase": "EE0000000000000000000002",
    "frameworks_phase": "EE0000000000000000000003",

    "target_debug_cfg": "FF0000000000000000000001",
    "target_release_cfg": "FF0000000000000000000002",
    "project_debug_cfg": "FF0000000000000000000003",
    "project_release_cfg": "FF0000000000000000000004",

    "target_cfg_list": "AB0000000000000000000001",
    "project_cfg_list": "AB0000000000000000000002",
}

BUNDLE_ID = "com.xfff0.tidewater"

PBXPROJ = f"""// !$*UTF8*$!
{{
	archiveVersion = 1;
	classes = {{
	}};
	objectVersion = 56;
	objects = {{

		{IDS['app_swift_build']} /* TidewaterApp.swift in Sources */ = {{isa = PBXBuildFile; fileRef = {IDS['app_swift_ref']} /* TidewaterApp.swift */; }};
		{IDS['content_swift_build']} /* ContentView.swift in Sources */ = {{isa = PBXBuildFile; fileRef = {IDS['content_swift_ref']} /* ContentView.swift */; }};
		{IDS['dist_build']} /* dist in Resources */ = {{isa = PBXBuildFile; fileRef = {IDS['dist_ref']} /* dist */; }};

		{IDS['app_swift_ref']} /* TidewaterApp.swift */ = {{isa = PBXFileReference; lastKnownFileType = sourcecode.swift; path = TidewaterApp.swift; sourceTree = "<group>"; }};
		{IDS['content_swift_ref']} /* ContentView.swift */ = {{isa = PBXFileReference; lastKnownFileType = sourcecode.swift; path = ContentView.swift; sourceTree = "<group>"; }};
		{IDS['infoplist_ref']} /* Info.plist */ = {{isa = PBXFileReference; lastKnownFileType = text.plist.xml; path = Info.plist; sourceTree = "<group>"; }};
		{IDS['dist_ref']} /* dist */ = {{isa = PBXFileReference; lastKnownFileType = folder; path = dist; sourceTree = "<group>"; }};
		{IDS['product_ref']} /* Tidewater.app */ = {{isa = PBXFileReference; explicitFileType = wrapper.application; includeInIndex = 0; path = Tidewater.app; sourceTree = BUILT_PRODUCTS_DIR; }};

		{IDS['root_group']} /* root */ = {{
			isa = PBXGroup;
			children = (
				{IDS['app_group']} /* TidewaterApp */,
				{IDS['products_group']} /* Products */,
			);
			sourceTree = "<group>";
		}};
		{IDS['app_group']} /* TidewaterApp */ = {{
			isa = PBXGroup;
			children = (
				{IDS['app_swift_ref']} /* TidewaterApp.swift */,
				{IDS['content_swift_ref']} /* ContentView.swift */,
				{IDS['infoplist_ref']} /* Info.plist */,
				{IDS['dist_ref']} /* dist */,
			);
			path = TidewaterApp;
			sourceTree = "<group>";
		}};
		{IDS['products_group']} /* Products */ = {{
			isa = PBXGroup;
			children = (
				{IDS['product_ref']} /* Tidewater.app */,
			);
			name = Products;
			sourceTree = "<group>";
		}};

		{IDS['target']} /* Tidewater */ = {{
			isa = PBXNativeTarget;
			buildConfigurationList = {IDS['target_cfg_list']} /* Build configuration list for PBXNativeTarget "Tidewater" */;
			buildPhases = (
				{IDS['sources_phase']} /* Sources */,
				{IDS['frameworks_phase']} /* Frameworks */,
				{IDS['resources_phase']} /* Resources */,
			);
			buildRules = (
			);
			dependencies = (
			);
			name = Tidewater;
			productName = Tidewater;
			productReference = {IDS['product_ref']} /* Tidewater.app */;
			productType = "com.apple.product-type.application";
		}};

		{IDS['project']} /* Project object */ = {{
			isa = PBXProject;
			attributes = {{
				BuildIndependentTargetsInParallel = 1;
				LastSwiftUpdateCheck = 1600;
				LastUpgradeCheck = 1600;
			}};
			buildConfigurationList = {IDS['project_cfg_list']} /* Build configuration list for PBXProject "Tidewater" */;
			compatibilityVersion = "Xcode 14.0";
			developmentRegion = en;
			hasScannedForEncodings = 0;
			knownRegions = (
				en,
				Base,
			);
			mainGroup = {IDS['root_group']};
			productRefGroup = {IDS['products_group']} /* Products */;
			projectDirPath = "";
			projectRoot = "";
			targets = (
				{IDS['target']} /* Tidewater */,
			);
		}};

		{IDS['sources_phase']} /* Sources */ = {{
			isa = PBXSourcesBuildPhase;
			buildActionMask = 2147483647;
			files = (
				{IDS['app_swift_build']} /* TidewaterApp.swift in Sources */,
				{IDS['content_swift_build']} /* ContentView.swift in Sources */,
			);
			runOnlyForDeploymentPostprocessing = 0;
		}};
		{IDS['resources_phase']} /* Resources */ = {{
			isa = PBXResourcesBuildPhase;
			buildActionMask = 2147483647;
			files = (
				{IDS['dist_build']} /* dist in Resources */,
			);
			runOnlyForDeploymentPostprocessing = 0;
		}};
		{IDS['frameworks_phase']} /* Frameworks */ = {{
			isa = PBXFrameworksBuildPhase;
			buildActionMask = 2147483647;
			files = (
			);
			runOnlyForDeploymentPostprocessing = 0;
		}};

		{IDS['target_debug_cfg']} /* Debug */ = {{
			isa = XCBuildConfiguration;
			buildSettings = {{
				ASSETCATALOG_COMPILER_GENERATE_ASSET_SYMBOLS = NO;
				CODE_SIGN_STYLE = Manual;
				CODE_SIGNING_ALLOWED = NO;
				CODE_SIGNING_REQUIRED = NO;
				CODE_SIGN_IDENTITY = "";
				GENERATE_INFOPLIST_FILE = NO;
				INFOPLIST_FILE = TidewaterApp/Info.plist;
				IPHONEOS_DEPLOYMENT_TARGET = 17.0;
				LD_RUNPATH_SEARCH_PATHS = "$(inherited) @executable_path/Frameworks";
				PRODUCT_BUNDLE_IDENTIFIER = {BUNDLE_ID};
				PRODUCT_NAME = Tidewater;
				SDKROOT = iphoneos;
				SWIFT_EMIT_LOC_STRINGS = YES;
				SWIFT_VERSION = 5.0;
				TARGETED_DEVICE_FAMILY = "1,2";
			}};
			name = Debug;
		}};
		{IDS['target_release_cfg']} /* Release */ = {{
			isa = XCBuildConfiguration;
			buildSettings = {{
				ASSETCATALOG_COMPILER_GENERATE_ASSET_SYMBOLS = NO;
				CODE_SIGN_STYLE = Manual;
				CODE_SIGNING_ALLOWED = NO;
				CODE_SIGNING_REQUIRED = NO;
				CODE_SIGN_IDENTITY = "";
				GENERATE_INFOPLIST_FILE = NO;
				INFOPLIST_FILE = TidewaterApp/Info.plist;
				IPHONEOS_DEPLOYMENT_TARGET = 17.0;
				LD_RUNPATH_SEARCH_PATHS = "$(inherited) @executable_path/Frameworks";
				PRODUCT_BUNDLE_IDENTIFIER = {BUNDLE_ID};
				PRODUCT_NAME = Tidewater;
				SDKROOT = iphoneos;
				SWIFT_EMIT_LOC_STRINGS = YES;
				SWIFT_VERSION = 5.0;
				TARGETED_DEVICE_FAMILY = "1,2";
				VALIDATE_PRODUCT = YES;
			}};
			name = Release;
		}};
		{IDS['project_debug_cfg']} /* Debug */ = {{
			isa = XCBuildConfiguration;
			buildSettings = {{
				ALWAYS_SEARCH_USER_PATHS = NO;
				CLANG_ENABLE_MODULES = YES;
				CLANG_ENABLE_OBJC_ARC = YES;
				CODE_SIGNING_ALLOWED = NO;
				CODE_SIGNING_REQUIRED = NO;
				COPY_PHASE_STRIP = NO;
				DEBUG_INFORMATION_FORMAT = dwarf;
				ENABLE_STRICT_OBJC_MSGSEND = YES;
				ENABLE_TESTABILITY = YES;
				GCC_C_LANGUAGE_STANDARD = gnu17;
				GCC_DYNAMIC_NO_PIC = NO;
				GCC_OPTIMIZATION_LEVEL = 0;
				GCC_PREPROCESSOR_DEFINITIONS = (
					"DEBUG=1",
					"$(inherited)",
				);
				MTL_ENABLE_DEBUG_INFO = INCLUDE_SOURCE;
				ONLY_ACTIVE_ARCH = YES;
				SWIFT_ACTIVE_COMPILATION_CONDITIONS = DEBUG;
				SWIFT_OPTIMIZATION_LEVEL = "-Onone";
			}};
			name = Debug;
		}};
		{IDS['project_release_cfg']} /* Release */ = {{
			isa = XCBuildConfiguration;
			buildSettings = {{
				ALWAYS_SEARCH_USER_PATHS = NO;
				CLANG_ENABLE_MODULES = YES;
				CLANG_ENABLE_OBJC_ARC = YES;
				CODE_SIGNING_ALLOWED = NO;
				CODE_SIGNING_REQUIRED = NO;
				COPY_PHASE_STRIP = NO;
				DEBUG_INFORMATION_FORMAT = "dwarf-with-dsym";
				ENABLE_NS_ASSERTIONS = NO;
				ENABLE_STRICT_OBJC_MSGSEND = YES;
				GCC_C_LANGUAGE_STANDARD = gnu17;
				MTL_ENABLE_DEBUG_INFO = NO;
				SWIFT_COMPILATION_MODE = wholemodule;
				SWIFT_OPTIMIZATION_LEVEL = "-O";
				VALIDATE_PRODUCT = YES;
			}};
			name = Release;
		}};

		{IDS['target_cfg_list']} /* Build configuration list for PBXNativeTarget "Tidewater" */ = {{
			isa = XCConfigurationList;
			buildConfigurations = (
				{IDS['target_debug_cfg']} /* Debug */,
				{IDS['target_release_cfg']} /* Release */,
			);
			defaultConfigurationIsVisible = 0;
			defaultConfigurationName = Release;
		}};
		{IDS['project_cfg_list']} /* Build configuration list for PBXProject "Tidewater" */ = {{
			isa = XCConfigurationList;
			buildConfigurations = (
				{IDS['project_debug_cfg']} /* Debug */,
				{IDS['project_release_cfg']} /* Release */,
			);
			defaultConfigurationIsVisible = 0;
			defaultConfigurationName = Release;
		}};
	}};
	rootObject = {IDS['project']} /* Project object */;
}}
"""

if __name__ == "__main__":
    out_dir = os.path.join(os.path.dirname(__file__), "Tidewater.xcodeproj")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "project.pbxproj")
    with open(out_path, "w") as f:
        f.write(PBXPROJ)
    print(f"wrote {out_path}")
