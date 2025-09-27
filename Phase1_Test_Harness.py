#!/usr/bin/env python3
"""
Phase 1 Test Harness - Individual Function Testing
Tests each broken color operation function to verify failures and later test fixes.
"""

import sys
import os
import traceback

# Add the src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    import DaVinciResolveScript as dvr_script
    from api.color_operations import (
        get_current_node,
        apply_lut,
        add_node,
        copy_grade,
        get_color_wheels,
        set_color_wheel_param
    )
except ImportError as e:
    print(f"❌ Import Error: {e}")
    print("Make sure DaVinci Resolve is running and RESOLVE_SCRIPT_API is set")
    sys.exit(1)

class ColorOperationsTestHarness:
    """Test harness for individual color operations functions"""
    
    def __init__(self):
        self.resolve = None
        self.test_results = {}
        
    def setup(self):
        """Initialize connection to DaVinci Resolve"""
        print("🔧 Setting up test environment...")
        
        try:
            self.resolve = dvr_script.scriptapp("Resolve")
            if not self.resolve:
                print("❌ Could not connect to DaVinci Resolve")
                return False
                
            project = self.resolve.GetProjectManager().GetCurrentProject()
            if not project:
                print("❌ No project open")
                return False
                
            timeline = project.GetCurrentTimeline()
            if not timeline:
                print("❌ No timeline open")
                return False
                
            current_item = timeline.GetCurrentVideoItem()
            if not current_item:
                print("❌ No video item selected")
                return False
                
            print(f"✅ Connected to project: {project.GetName()}")
            print(f"✅ Timeline: {timeline.GetName()}")
            print(f"✅ Clip: {current_item.GetName()}")
            return True
            
        except Exception as e:
            print(f"❌ Setup error: {e}")
            return False
    
    def test_function(self, func_name, func, *args, **kwargs):
        """Test a single function and record results"""
        print(f"\n🧪 Testing {func_name}...")
        
        try:
            result = func(self.resolve, *args, **kwargs)
            
            # Check if result indicates success or failure
            if isinstance(result, dict):
                if "error" in result:
                    print(f"   ❌ FAILED: {result['error']}")
                    self.test_results[func_name] = {
                        "status": "FAILED", 
                        "error": result["error"],
                        "type": "dict_error"
                    }
                else:
                    print(f"   ✅ SUCCESS: {result}")
                    self.test_results[func_name] = {
                        "status": "SUCCESS",
                        "result": result
                    }
            elif isinstance(result, str):
                if result.startswith("Error"):
                    print(f"   ❌ FAILED: {result}")
                    self.test_results[func_name] = {
                        "status": "FAILED",
                        "error": result,
                        "type": "string_error"
                    }
                else:
                    print(f"   ✅ SUCCESS: {result}")
                    self.test_results[func_name] = {
                        "status": "SUCCESS", 
                        "result": result
                    }
            else:
                print(f"   ✅ SUCCESS: {result}")
                self.test_results[func_name] = {
                    "status": "SUCCESS",
                    "result": result
                }
                
        except Exception as e:
            error_details = f"{type(e).__name__}: {str(e)}"
            print(f"   ❌ EXCEPTION: {error_details}")
            
            # Check if it's the expected NoneType error
            if "'NoneType' object" in str(e):
                print("   🎯 CONFIRMED: This is the expected NoneType error from GetCurrentGrade()")
            
            self.test_results[func_name] = {
                "status": "EXCEPTION",
                "error": error_details,
                "traceback": traceback.format_exc()
            }
    
    def run_all_tests(self):
        """Run tests for all broken functions"""
        
        print("🚀 Starting Color Operations Test Suite")
        print("=" * 60)
        
        if not self.setup():
            return False
        
        # Test 1: get_current_node
        self.test_function("get_current_node", get_current_node)
        
        # Test 2: apply_lut (with a dummy LUT path)
        # Create a dummy LUT file for testing
        dummy_lut_path = "/tmp/test.cube"
        try:
            with open(dummy_lut_path, 'w') as f:
                f.write("# Test LUT file\\nLUT_3D_SIZE 2\\n0.0 0.0 0.0\\n1.0 1.0 1.0\\n")
            self.test_function("apply_lut", apply_lut, dummy_lut_path)
        except Exception as e:
            print(f"   ⚠️ Could not create test LUT file: {e}")
            self.test_function("apply_lut", apply_lut, "nonexistent.cube")
        
        # Test 3: add_node
        self.test_function("add_node_serial", add_node, "serial", "Test Node")
        
        # Test 4: copy_grade (will fail because no source/target specified correctly)
        self.test_function("copy_grade", copy_grade)
        
        # Test 5: get_color_wheels
        self.test_function("get_color_wheels", get_color_wheels)
        
        # Test 6: set_color_wheel_param
        self.test_function("set_color_wheel_param", set_color_wheel_param, "lift", "red", 0.1)
        
        return True
    
    def print_summary(self):
        """Print test results summary"""
        
        print("\\n" + "=" * 60)
        print("📊 TEST RESULTS SUMMARY")
        print("=" * 60)
        
        total_tests = len(self.test_results)
        failed_tests = sum(1 for result in self.test_results.values() if result["status"] in ["FAILED", "EXCEPTION"])
        success_tests = total_tests - failed_tests
        
        print(f"Total Tests: {total_tests}")
        print(f"✅ Successful: {success_tests}")  
        print(f"❌ Failed: {failed_tests}")
        print()
        
        # Detailed results
        for func_name, result in self.test_results.items():
            status_icon = "✅" if result["status"] == "SUCCESS" else "❌"
            print(f"{status_icon} {func_name}: {result['status']}")
            
            if result["status"] in ["FAILED", "EXCEPTION"]:
                print(f"   Error: {result.get('error', 'Unknown error')}")
                
                # Check for NoneType errors specifically
                if "'NoneType' object" in result.get('error', ''):
                    print(f"   🎯 ROOT CAUSE: GetCurrentGrade() returns None")
                print()
        
        # Analysis
        print("🔍 ANALYSIS:")
        nonetype_errors = sum(1 for r in self.test_results.values() 
                            if "'NoneType' object" in r.get('error', ''))
        
        if nonetype_errors > 0:
            print(f"   • {nonetype_errors} functions failing due to GetCurrentGrade() returning None")
            print(f"   • This confirms that Grade object methods don't exist in the API")
            print(f"   • All color operations need to be rewritten using CDL/NodeGraph APIs")
        
        print(f"   • {failed_tests}/{total_tests} functions are completely broken")
        print(f"   • Phase 2-3 implementation will fix these using working API methods")

def main():
    """Main test execution"""
    
    print("🎨 DaVinci Resolve Color Operations Test Harness")
    print("Phase 1: Verify Current Broken State")
    print("=" * 60)
    
    harness = ColorOperationsTestHarness()
    
    if harness.run_all_tests():
        harness.print_summary()
        
        # Save results to file
        import json
        with open("Phase1_Test_Results.json", "w") as f:
            json.dump(harness.test_results, f, indent=2)
        print(f"\\n📁 Test results saved to Phase1_Test_Results.json")
        
        # Determine exit code
        failed_count = sum(1 for result in harness.test_results.values() 
                          if result["status"] in ["FAILED", "EXCEPTION"])
        
        if failed_count == len(harness.test_results):
            print("\\n🎯 EXPECTED RESULT: All functions failed (as expected for Phase 1)")
            print("   This confirms the scope of the problem and validates our approach")
            return 0  # Success - we expected everything to fail
        else:
            print("\\n⚠️ UNEXPECTED: Some functions worked - investigation needed")  
            return 1
    else:
        print("\\n❌ Could not run tests - check DaVinci Resolve setup")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)