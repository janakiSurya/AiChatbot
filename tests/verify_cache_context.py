from core.chat_engine import ChatEngine
from utils.session_manager import session_manager
from utils.redis_cache import RedisSemanticCache
import time

print('Initializing...')
engine = ChatEngine()
engine.initialize()
cache = RedisSemanticCache()

# Clear cache
if cache.is_connected and cache.redis:
    keys = cache.redis.keys('cache:*')
    if keys:
        for key in keys:
            cache.redis.delete(key)
    print('✅ Cache cleared')
else:
    print('⚠️ Redis not connected')

session = session_manager.generate_session_id()
print(f'Session ID: {session}\n')

def ask(q):
    r = ''
    try:
        for chunk in engine.chat_stream(q, session_id=session):
            r += chunk
    except Exception as e:
        print(f"Error: {e}")
    return r

def get_cache_count():
    if cache.is_connected and cache.redis:
        return len(cache.redis.keys('cache:*'))
    return 0

# Test 1: Standalone
print('1. Standalone: Does he know AWS?')
r1 = ask('Does he know AWS?')
c1 = get_cache_count()
print(f'Cache entries: {c1}')
if c1 >= 1:
    print('✅ PASS: Response cached')
else:
    print('❌ FAIL: Response NOT cached')

# Test 2: Follow-up
print('\n2. Follow-up: Which project used that skill?')
r2 = ask('Which project used that skill?')
c2 = get_cache_count()
print(f'Cache entries: {c2}')
if c2 == c1:
    print('✅ PASS: Follow-up NOT cached (count stayed same)')
else:
    print(f'❌ FAIL: Follow-up cached (count increased by {c2-c1})')

# Test 3: Context Check
has_aws = 'aws' in r2.lower() or 'cloud' in r2.lower()
print(f'\n3. Context Check: Response mentions AWS?')
if has_aws:
    print(f'✅ PASS: found AWS context. Preview: {r2[:100]}...')
else:
    print(f'❌ FAIL: no AWS context found. Response: {r2[:100]}...')
