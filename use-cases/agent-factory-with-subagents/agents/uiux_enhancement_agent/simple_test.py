# -*- coding: utf-8 -*-
"""
Simple test MCP integration for UI/UX Enhancement Agent.
"""

import sys
from pathlib import Path

# Add paths
sys.path.append(str(Path(__file__).parent))
sys.path.append(str(Path(__file__).parent.parent.parent / "shared"))

def test_mcp_dependencies():
    """Test MCP dependencies creation."""
    try:
        from dependencies import UIUXEnhancementDependencies

        print("TESTING MCP DEPENDENCIES")
        print("=" * 50)

        # Create dependencies
        deps = UIUXEnhancementDependencies(
            api_key="test_key",
            domain_type="ecommerce",
            project_type="web_application",
            design_system_type="shadcn/ui",
            css_framework="tailwind"
        )

        print(f"Created: {deps.__class__.__name__}")
        print(f"MCP Enabled: {deps.enable_mcp_integration}")
        print(f"MCP Servers: {deps.custom_mcp_servers}")
        print(f"Working Dir: {deps.mcp_working_dir}")

        # Test MCP integration
        mcp_integration = deps.get_mcp_integration()

        if mcp_integration:
            print(f"MCP Integration: SUCCESS")
            print(f"Available servers: {list(mcp_integration.servers.keys())}")
        else:
            print("MCP Integration: DISABLED")

        print("=" * 50)
        print("TEST PASSED: Dependencies work correctly")
        return True

    except Exception as e:
        print(f"TEST FAILED: {e}")
        return False

def test_mcp_toolsets():
    """Test MCP toolsets."""
    try:
        from dependencies import UIUXEnhancementDependencies

        print("\nTESTING MCP TOOLSETS")
        print("=" * 50)

        deps = UIUXEnhancementDependencies(
            api_key="test_key",
            domain_type="ui"
        )

        # Get toolsets
        toolsets = deps.get_mcp_toolsets()

        print(f"Toolsets retrieved: {len(toolsets) if toolsets else 0}")

        if toolsets:
            print("MCP Toolsets: AVAILABLE")
        else:
            print("MCP Toolsets: FALLBACK MODE (normal without servers)")

        print("=" * 50)
        print("TEST PASSED: Toolsets work correctly")
        return True

    except Exception as e:
        print(f"TEST FAILED: {e}")
        return False

if __name__ == "__main__":
    print("MCP INTEGRATION TESTING")
    print("=" * 60)

    results = []

    # Test 1: Dependencies
    results.append(test_mcp_dependencies())

    # Test 2: Toolsets
    results.append(test_mcp_toolsets())

    # Summary
    passed = sum(results)
    total = len(results)

    print(f"\nRESULTS: {passed}/{total} tests passed")

    if passed == total:
        print("SUCCESS: All tests passed!")
        exit(0)
    else:
        print("FAILURE: Some tests failed!")
        exit(1)