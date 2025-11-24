"""
Test markdown cleanup and formatting
"""

import sys
import os
import re
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_markdown_cleanup():
    """Test that markdown formatting is properly removed"""
    
    # Simulate the _clean_response method
    def clean_response(text):
        """Basic cleanup of the response"""
        if not text:
            return ""
            
        # Remove citation markers
        text = re.sub(r'\[Info\s*\d+\]', '', text)
        text = re.sub(r'\[\d+\]', '', text)
        text = re.sub(r'\[Source\s*\d+\]', '', text, flags=re.IGNORECASE)
        
        # Remove markdown formatting
        text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)  # **bold**
        text = re.sub(r'__([^_]+)__', r'\1', text)  # __bold__
        text = re.sub(r'\*([^*]+)\*', r'\1', text)  # *italic*
        text = re.sub(r'_([^_]+)_', r'\1', text)  # _italic_
        text = re.sub(r'~~([^~]+)~~', r'\1', text)  # ~~strike~~
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    print("\n" + "="*60)
    print("Testing Markdown & Citation Cleanup")
    print("="*60)
    
    test_cases = [
        {
            "name": "Bold markdown",
            "input": "Surya has **over 4 years of experience** as a developer",
            "expected": "Surya has over 4 years of experience as a developer"
        },
        {
            "name": "Bold + Citation",
            "input": "Surya has **over 4 years of experience**[Info1] building apps",
            "expected": "Surya has over 4 years of experience building apps"
        },
        {
            "name": "Multiple formatting",
            "input": "He's **really good** at *Python* and __JavaScript__",
            "expected": "He's really good at Python and JavaScript"
        },
        {
            "name": "Strikethrough",
            "input": "He ~~doesn't~~ works with React",
            "expected": "He doesn't works with React"
        },
        {
            "name": "Clean text",
            "input": "Surya works at Acer America",
            "expected": "Surya works at Acer America"
        }
    ]
    
    all_passed = True
    
    for test in test_cases:
        result = clean_response(test["input"])
        passed = result == test["expected"]
        
        print(f"\n{test['name']}: {'✅ PASS' if passed else '❌ FAIL'}")
        print(f"  Input:    {test['input']}")
        print(f"  Expected: {test['expected']}")
        print(f"  Got:      {result}")
        
        if not passed:
            all_passed = False
    
    print("\n" + "="*60)
    if all_passed:
        print("✅ All tests passed!")
    else:
        print("❌ Some tests failed")
    print("="*60)
    
    return all_passed


if __name__ == "__main__":
    success = test_markdown_cleanup()
    sys.exit(0 if success else 1)
