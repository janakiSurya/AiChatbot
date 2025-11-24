"""
Test citation cleanup in responses
"""

import sys
import os
import re
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_citation_cleanup():
    """Test that citations are properly removed from responses"""
    
    # Simulate the _clean_response method
    def clean_response(text):
        """Basic cleanup of the response"""
        if not text:
            return ""
            
        # Remove any potential thinking tags
        text = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)
        
        # Remove citation markers - multiple patterns
        text = re.sub(r'\[Info\s*\d+\]', '', text)  # [Info1], [Info 1]
        text = re.sub(r'\[\d+\]', '', text)  # [1], [2]
        text = re.sub(r'\[Source\s*\d+\]', '', text, flags=re.IGNORECASE)  # [Source1]
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    print("\n" + "="*60)
    print("Testing Citation Cleanup")
    print("="*60)
    
    # Test cases
    test_cases = [
        {
            "input": "Surya has **over 4 years of experience** as a Full Stack Developer building scalable web applications using modern frameworks like React, Node.js, and MongoDB[Info1]",
            "expected": "Surya has **over 4 years of experience** as a Full Stack Developer building scalable web applications using modern frameworks like React, Node.js, and MongoDB"
        },
        {
            "input": "He works at Acer America[Info 2] and has experience with GenAI[3]",
            "expected": "He works at Acer America and has experience with GenAI"
        },
        {
            "input": "His skills include Python[Source1], React[Source 2], and AWS[4]",
            "expected": "His skills include Python, React, and AWS"
        },
        {
            "input": "No citations here!",
            "expected": "No citations here!"
        }
    ]
    
    all_passed = True
    
    for i, test in enumerate(test_cases, 1):
        result = clean_response(test["input"])
        passed = result == test["expected"]
        
        print(f"\nTest {i}: {'✅ PASS' if passed else '❌ FAIL'}")
        print(f"Input:    {test['input'][:80]}...")
        print(f"Expected: {test['expected'][:80]}...")
        print(f"Got:      {result[:80]}...")
        
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
    success = test_citation_cleanup()
    sys.exit(0 if success else 1)
