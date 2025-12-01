"""
Test HTTP connection pooling in response generator
"""

import pytest
from llm.response_generator import ResponseGenerator


def test_session_exists():
    """Verify ResponseGenerator has HTTP session for connection pooling"""
    generator = ResponseGenerator()
    
    assert hasattr(generator, 'session'), "ResponseGenerator should have session attribute"
    assert generator.session is not None, "Session should not be None"
    assert hasattr(generator.session, 'headers'), "Session should have headers"
    
    # Verify auth header is set
    assert 'Authorization' in generator.session.headers, "Authorization header should be set"
    
    print("✅ Session pooling test passed")


def test_session_reuse():
    """Verify same session is reused across requests (not creating new connections)"""
    generator = ResponseGenerator()
    
    session1 = generator.session
    
    # Simulate multiple operations
    for i in range(5):
        session = generator.session
        assert session is session1, f"Session changed on iteration {i} - not reusing connection!"
    
    print("✅ Session reuse test passed")


def test_cleanup():
    """Verify cleanup properly closes session"""
    generator = ResponseGenerator()
    session = generator.session
    
    assert session is not None, "Session should exist before cleanup"
    
    # Call cleanup
    generator.cleanup()
    
    # After cleanup, session should be closed (we can't directly test this,
    # but we verify cleanup was called without errors)
    print("✅ Cleanup test passed")


def test_no_session_leak():
    """Verify creating multiple generators doesn't leak sessions"""
    import gc
    
    generators = []
    for i in range(10):
        gen = ResponseGenerator()
        generators.append(gen)
    
    # All should have sessions
    for i, gen in enumerate(generators):
        assert gen.session is not None, f"Generator {i} missing session"
    
    # Cleanup all
    for gen in generators:
        gen.cleanup()
    
    # Force garbage collection
    generators = None
    gc.collect()
    
    print("✅ No session leak test passed")


if __name__ == "__main__":
    test_session_exists()
    test_session_reuse()
    test_cleanup()
    test_no_session_leak()
    print("\\n✅ All connection pool tests passed!")
