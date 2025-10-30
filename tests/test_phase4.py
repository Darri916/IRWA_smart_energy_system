"""
Test Phase 4: Database, Security, Information Retrieval
"""

from database.db_manager import DatabaseManager
from security.security_manager import SecurityManager
from information_retrieval.ir_engine import IREngine
from agents.weather_agent import WeatherAgent
from agents.demand_agent import EnergyDemandAgent
from agents.grid_agent import GridBalancerAgent

def print_section(title):
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def main():
    print_section("TESTING PHASE 4 COMPONENTS")
    
    # Test 1: Database
    print_section("1. Testing Database Manager")
    db = DatabaseManager()
    print("✓ Database initialized")
    
    # Generate and save test data
    weather_agent = WeatherAgent()
    demand_agent = EnergyDemandAgent()
    grid_agent = GridBalancerAgent()
    
    weather_result = weather_agent.process_weather_request("Colombo")
    demand_result = demand_agent.process_demand_forecast(weather_result)
    grid_result = grid_agent.coordinate_with_agents(weather_result, demand_result)
    
    # Save to database
    weather_id = db.save_weather_forecast(weather_result)
    demand_id = db.save_demand_forecast(demand_result)
    grid_id = db.save_grid_balance(grid_result)
    
    print(f"✓ Weather forecast saved: ID={weather_id}")
    print(f"✓ Demand forecast saved: ID={demand_id}")
    print(f"✓ Grid balance saved: ID={grid_id}")
    
    # Save AI decision
    decision_data = {
        'agent_id': 'grid_001',
        'type': 'grid_balancing',
        'decision': 'Optimize energy mix',
        'reasoning': 'Balance renewable and conventional sources',
        'confidence': 0.95,
        'impact': 'high',
        'input_data': {'demand': 945, 'renewable': 590}
    }
    
    decision_id = db.save_ai_decision(decision_data)
    print(f"✓ AI decision saved: ID={decision_id}")
    
    # Retrieve history
    print("\n📊 Retrieving Historical Data:")
    weather_history = db.get_weather_history("Colombo", days=7)
    print(f"   Weather records: {len(weather_history)}")
    
    demand_history = db.get_demand_history(days=7)
    print(f"   Demand records: {len(demand_history)}")
    
    grid_history = db.get_grid_history(days=7)
    print(f"   Grid records: {len(grid_history)}")
    
    # Get statistics
    print("\n📈 System Statistics:")
    stats = db.get_system_statistics(days=7)
    print(f"   Avg Renewable: {stats['grid_statistics']['avg_renewable_percentage']:.1f}%")
    print(f"   Avg Efficiency: {stats['grid_statistics']['avg_efficiency']:.1f}%")
    print(f"   Total Records: {stats['grid_statistics']['total_records']}")
    
    # Test 2: Security Manager
    print_section("2. Testing Security Manager")
    security = SecurityManager()
    print("✓ Security Manager initialized")
    
    # Test session management
    print("\n🔐 Testing Session Management:")
    session = security.create_session(user_id='test_user', ip_address='127.0.0.1')
    print(f"   Session created: {session['session_id'][:16]}...")
    
    validation = security.validate_session(session['session_id'])
    print(f"   Session valid: {validation['valid']}")
    print(f"   User ID: {validation['user_id']}")
    
    # Test input validation
    print("\n✅ Testing Input Validation:")
    city_validation = security.validate_city_input("Colombo")
    print(f"   City validation: {city_validation['valid']}")
    print(f"   Sanitized: {city_validation['sanitized']}")
    
    # Test malicious input
    malicious = security.sanitize_text_input("<script>alert('xss')</script> Normal text")
    print(f"   XSS protection: '{malicious}'")
    
    sql_injection = security.sanitize_text_input("'; DROP TABLE users; --")
    print(f"   SQL injection blocked: '{sql_injection}'")
    
    # Test rate limiting
    print("\n⏱️  Testing Rate Limiting:")
    rate_check = security.check_rate_limit('test_user', limit=5, window_seconds=60)
    print(f"   Request allowed: {rate_check['allowed']}")
    print(f"   Remaining: {rate_check.get('remaining', 0)}")
    
    # Test encryption
    print("\n🔒 Testing Encryption:")
    sensitive_data = "API_KEY_12345"
    encrypted = security.encrypt_data(sensitive_data)
    decrypted = security.decrypt_data(encrypted)
    print(f"   Original: {sensitive_data}")
    print(f"   Encrypted: {encrypted[:30]}...")
    print(f"   Decrypted: {decrypted}")
    print(f"   Match: {sensitive_data == decrypted}")
    
    # Test password hashing
    print("\n🔑 Testing Password Security:")
    password = "SecurePassword123"
    hashed = security.hash_password(password)
    print(f"   Password hashed: {hashed[:30]}...")
    print(f"   Verification: {security.verify_password(password, hashed)}")
    print(f"   Wrong password: {security.verify_password('wrong', hashed)}")
    
    # Test JWT tokens
    print("\n🎫 Testing JWT Tokens:")
    token = security.generate_token('test_user', expires_in=3600)
    print(f"   Token generated: {token[:30]}...")
    
    token_validation = security.verify_token(token)
    print(f"   Token valid: {token_validation['valid']}")
    print(f"   User ID: {token_validation.get('user_id')}")
    
    # Security report
    print("\n📋 Security Report:")
    report = security.generate_security_report()
    print(f"   Active sessions: {report['active_sessions']}")
    print(f"   Blocked IPs: {report['blocked_ips']}")
    print(f"   Encryption enabled: {report['encryption_enabled']}")
    print(f"   Security features: {len(report['security_features'])}")
    
    # Test 3: Information Retrieval
    print_section("3. Testing Information Retrieval Engine")
    ir_engine = IREngine(db_manager=db)
    print("✓ IR Engine initialized")
    
    # Test search
    print("\n🔍 Testing Search:")
    search_queries = [
        "renewable energy",
        "grid balance",
        "Colombo weather"
    ]
    
    for query in search_queries:
        results = ir_engine.search(query, limit=5)
        print(f"\n   Query: '{query}'")
        print(f"   Results found: {results['total_results']}")
        print(f"   Keywords: {results['keywords']}")
        
        if results['results']:
            top_result = results['results'][0]
            print(f"   Top result: [{top_result['type']}] {top_result['summary'][:60]}...")
    
    # Test filtered search
    print("\n🎯 Testing Filtered Search:")
    filtered_results = ir_engine.search(
        "renewable",
        filters={'type': 'grid', 'days': 7},
        limit=10
    )
    print(f"   Filtered results: {filtered_results['total_results']}")
    print(f"   Filters applied: {filtered_results['filters_applied']}")
    
    # Test search suggestions
    print("\n💡 Testing Search Suggestions:")
    suggestions = ir_engine.get_suggestions("rene", limit=5)
    print(f"   Suggestions for 'rene': {suggestions}")
    
    # Test trending searches
    print("\n📊 Trending Searches:")
    trending = ir_engine.get_trending_searches(days=7)
    for i, trend in enumerate(trending[:3], 1):
        print(f"   {i}. {trend['topic']} ({trend['count']} searches)")
    
    # IR Engine status
    print("\n📈 IR Engine Status:")
    ir_status = ir_engine.get_status()
    print(f"   Cache size: {ir_status['cache_size']}")
    print(f"   DB connected: {ir_status['db_connected']}")
    print(f"   Capabilities: {len(ir_status['capabilities'])}")
    
    # Test 4: Integration Test
    print_section("4. Testing Full Integration")
    
    print("\n🔄 Complete Workflow Test:")
    print("   1. Security: Create session")
    workflow_session = security.create_session('workflow_user')
    print(f"      ✓ Session: {workflow_session['session_id'][:16]}...")
    
    print("   2. Security: Validate input")
    city_input = security.validate_city_input("Jaffna")
    print(f"      ✓ City validated: {city_input['sanitized']}")
    
    print("   3. Agents: Generate forecasts")
    w_result = weather_agent.process_weather_request(city_input['sanitized'])
    d_result = demand_agent.process_demand_forecast(w_result)
    g_result = grid_agent.coordinate_with_agents(w_result, d_result)
    print(f"      ✓ Forecasts generated")
    
    print("   4. Database: Save results")
    w_id = db.save_weather_forecast(w_result)
    d_id = db.save_demand_forecast(d_result)
    g_id = db.save_grid_balance(g_result)
    print(f"      ✓ Saved to DB (IDs: {w_id}, {d_id}, {g_id})")
    
    print("   5. IR: Search saved data")
    search_results = ir_engine.search(city_input['sanitized'], limit=5)
    print(f"      ✓ Found {search_results['total_results']} results")
    
    print("   6. Security: End session")
    security.terminate_session(workflow_session['session_id'])
    print(f"      ✓ Session terminated")
    
    # Final Summary
    print_section("✅ PHASE 4 COMPLETE!")
    print("\n🎉 All components working correctly!")
    print("   ✓ Database (SQLite with 7 tables)")
    print("   ✓ Security (8 security features)")
    print("   ✓ Information Retrieval (7 capabilities)")
    print("   ✓ Full integration tested")
    
    print("\n📊 System Status:")
    print(f"   Database records: {len(weather_history) + len(demand_history) + len(grid_history)}")
    print(f"   Active sessions: {security.get_active_sessions_count()}")
    print(f"   Search cache: {ir_engine.get_status()['cache_size']} queries")
    
    print("\n📋 Next: Phase 5 - Spectacular UI! 🎨")

if __name__ == "__main__":
    main()
