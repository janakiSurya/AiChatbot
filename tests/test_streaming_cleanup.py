"""
Test streaming cleanup logic
"""

import sys
import os
import re
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class MockResponseGenerator:
    def _clean_streaming_buffer(self, buffer):
        """
        Clean complete patterns from streaming buffer
        Returns: (cleaned_text_to_yield, remaining_buffer)
        """
        # Look for complete patterns to clean
        
        # Remove complete citation patterns
        cleaned = re.sub(r'\[Info\s*\d+\]', '', buffer)
        cleaned = re.sub(r'\[\d+\]', '', cleaned)
        cleaned = re.sub(r'\[Source\s*\d+\]', '', cleaned, flags=re.IGNORECASE)
        
        # Remove complete markdown patterns
        cleaned = re.sub(r'\*\*([^*]+)\*\*', r'\1', cleaned)
        cleaned = re.sub(r'__([^_]+)__', r'\1', cleaned)
        cleaned = re.sub(r'\*([^*]+)\*', r'\1', cleaned)
        cleaned = re.sub(r'_([^_]+)_', r'\1', cleaned)
        cleaned = re.sub(r'~~([^~]+)~~', r'\1', cleaned)
        
        # Check for incomplete patterns at the end
        # We need to keep any potential start of a pattern in the buffer
        
        # Check for incomplete citation: ends with [ but no ]
        last_open_bracket = cleaned.rfind('[')
        last_close_bracket = cleaned.rfind(']')
        
        if last_open_bracket != -1 and last_open_bracket > last_close_bracket:
            # Potential start of citation
            suffix = cleaned[last_open_bracket:]
            if re.match(r'\[(Info|Source|\d+)?', suffix, flags=re.IGNORECASE):
                return cleaned[:last_open_bracket], suffix
        
        # Check for incomplete markdown
        
        # Bold (**): odd number of **
        if cleaned.count('**') % 2 != 0:
            last_marker = cleaned.rfind('**')
            return cleaned[:last_marker], cleaned[last_marker:]
            
        # Underline/Bold (__): odd number of __
        if cleaned.count('__') % 2 != 0:
            last_marker = cleaned.rfind('__')
            return cleaned[:last_marker], cleaned[last_marker:]
            
        # Strikethrough (~~): odd number of ~~
        if cleaned.count('~~') % 2 != 0:
            last_marker = cleaned.rfind('~~')
            return cleaned[:last_marker], cleaned[last_marker:]
            
        # Italic (*): odd number of * (excluding **)
        # We replace ** with placeholders to count single * correctly
        temp_cleaned = cleaned.replace('**', '')
        if temp_cleaned.count('*') % 2 != 0:
            last_marker = cleaned.rfind('*')
            # Ensure this * isn't part of a **
            while last_marker > 0 and cleaned[last_marker-1] == '*':
                last_marker = cleaned.rfind('*', 0, last_marker-1)
            return cleaned[:last_marker], cleaned[last_marker:]
            
        # Italic (_): odd number of _ (excluding __)
        temp_cleaned = cleaned.replace('__', '')
        if temp_cleaned.count('_') % 2 != 0:
            last_marker = cleaned.rfind('_')
            while last_marker > 0 and cleaned[last_marker-1] == '_':
                last_marker = cleaned.rfind('_', 0, last_marker-1)
            return cleaned[:last_marker], cleaned[last_marker:]
        
        return cleaned, ""

def test_streaming_cleanup():
    """Test streaming cleanup logic"""
    print("\n" + "="*60)
    print("Testing Streaming Cleanup Logic")
    print("="*60)
    
    generator = MockResponseGenerator()
    
    test_cases = [
        {
            "name": "Split citation",
            "chunks": ["Surya has experience", "[Info", "1] in Python."],
            "expected": "Surya has experience in Python."
        },
        {
            "name": "Split bold",
            "chunks": ["He is **very", "** good."],
            "expected": "He is very good."
        },
        {
            "name": "Mixed split",
            "chunks": ["Skills: **Py", "thon**[1", "]"],
            "expected": "Skills: Python"
        },
        {
            "name": "Normal text",
            "chunks": ["Hello ", "world!"],
            "expected": "Hello world!"
        }
    ]
    
    all_passed = True
    
    for test in test_cases:
        print(f"\nTest: {test['name']}")
        buffer = ""
        output = ""
        
        for chunk in test['chunks']:
            buffer += chunk
            cleaned, buffer = generator._clean_streaming_buffer(buffer)
            output += cleaned
            # print(f"  Chunk: '{chunk}' -> Output: '{cleaned}', Buffer: '{buffer}'")
            
        # Flush remaining buffer
        if buffer:
            # In real code we'd call _clean_chunk here, but for this test just append
             # Remove complete citation patterns
            cleaned = re.sub(r'\[Info\s*\d+\]', '', buffer)
            cleaned = re.sub(r'\[\d+\]', '', cleaned)
            cleaned = re.sub(r'\[Source\s*\d+\]', '', cleaned, flags=re.IGNORECASE)
            
            # Remove complete markdown patterns
            cleaned = re.sub(r'\*\*([^*]+)\*\*', r'\1', cleaned)
            cleaned = re.sub(r'__([^_]+)__', r'\1', cleaned)
            cleaned = re.sub(r'\*([^*]+)\*', r'\1', cleaned)
            cleaned = re.sub(r'_([^_]+)_', r'\1', cleaned)
            cleaned = re.sub(r'~~([^~]+)~~', r'\1', cleaned)
            output += cleaned
            
        passed = output == test['expected']
        print(f"  Result: {'✅ PASS' if passed else '❌ FAIL'}")
        if not passed:
            print(f"  Expected: '{test['expected']}'")
            print(f"  Got:      '{output}'")
            all_passed = False
            
    print("\n" + "="*60)
    if all_passed:
        print("✅ All streaming tests passed!")
    else:
        print("❌ Some streaming tests failed")
    print("="*60)
    
    return all_passed

if __name__ == "__main__":
    success = test_streaming_cleanup()
    sys.exit(0 if success else 1)
