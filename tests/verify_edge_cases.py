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
    for key in cache.redis.keys('cache:*'):
        cache.redis.delete(key)
    print('✅ Cache cleared')

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

# --- PREVIOUS TESTS (Passed) ---
print('1. Standalone: Does he know AWS?')
ask('Does he know AWS?')
c1 = get_cache_count()

# --- EDGE CASE 1: Short Follow-up ("Tell me more") ---
print('\nEdge Case 1: Short Follow-up ("Tell me more")')
print('This should NOT be cached and should use context (AWS).')
r_short = ask('Tell me more')
c_short = get_cache_count()

if c_short == c1:
    print('✅ PASS: Cache skipped')
else:
    print('❌ FAIL: Cache increased')

if 'aws' in r_short.lower() or 'cloud' in r_short.lower():
    print('✅ PASS: Used context (mentioned AWS/Cloud)')
else:
    print('❌ FAIL: Lost context')

# --- EDGE CASE 2: Context Switch ("What about React?") ---
print('\nEdge Case 2: Context Switch ("What about React?")')
print('This Is a standalone question (mostly) but mentions a new topic.')
r_switch = ask('What about React?')
c_switch = get_cache_count()

# Note: "What about" is in vague list, so it might skip cache, 
# BUT it should definitely pick up React info.
if 'react' in r_switch.lower() or 'javascript' in r_switch.lower():
    print('✅ PASS: Found React info')
else:
    print('❌ FAIL: Failed to find React info')

# --- EDGE CASE 3: Ambiguous Reference ("work there") ---
print('\nEdge Case 3: Ambiguous Reference ("How long did he work there?")')
# "there" usually refers to the last mentioned entity (React/Company?)
r_ambiguous = ask('How long did he work there?')
c_ambiguous = get_cache_count()

if c_ambiguous == c_switch:
    print('✅ PASS: Cache skipped for "there"')
else:
    print('❌ FAIL: Cache increased for "there"')

print(f'\nFinal Cache Count: {get_cache_count()}')
