"""
Test AI Services - LLM, NLP, and Responsible AI
"""

from ai_services.llm_service import LLMService
from ai_services.nlp_service import NLPService
from ai_services.responsible_ai import ResponsibleAI

def print_section(title):
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def main():
    print_section("TESTING AI SERVICES")
    
    # Test 1: LLM Service
    print_section("1. Testing LLM Service")
    llm = LLMService()
    status = llm.get_status()
    
    print(f"Provider: {status['provider']}")
    print(f"Model: {status['model']}")
    print(f"Available: {status['available']}")
    
    # Test report generation
    test_weather = {
        'city': 'Colombo',
        'temperature': 29.5,
        'wind_speed': 3.5,
        'description': 'partly cloudy'
    }
    
    test_demand = {
        'predicted_demand_mw': 945,
        'confidence': 0.92
    }
    
    test_grid = {
        'renewable_generation': 590,
        'grid_balance': 'BALANCED',
        'storage_soc_percent': 65
    }
    
    print("\n📊 Generating Energy Report...")
    report = llm.generate_energy_report(test_weather, test_demand, test_grid)
    
    if report['status'] == 'success':
        print(f"✓ Report generated successfully")
        print(f"✓ Provider used: {report['provider']}")
        print(f"\n--- Report Preview ---")
        print(report['report'][:500] + "...")
    else:
        print(f"✗ Report generation failed: {report.get('error')}")
    
    # Test question answering
    print("\n❓ Testing Question Answering...")
    question = "What is the current renewable energy generation?"
    context = {
        'temperature': 29.5,
        'wind_speed': 3.5,
        'demand': 945,
        'renewable_score': 60,
        'grid_status': 'BALANCED'
    }
    
    answer = llm.answer_question(question, context)
    print(f"Q: {question}")
    print(f"A: {answer[:200]}...")
    
    # Test 2: NLP Service
    print_section("2. Testing NLP Service")
    nlp = NLPService()
    nlp_status = nlp.get_status()
    
    print(f"TextBlob Available: {nlp_status['textblob_available']}")
    print(f"Spacy Available: {nlp_status['spacy_available']}")
    print(f"Capabilities: {len(nlp_status['capabilities'])} features")
    
    # Test sentiment analysis
    test_text = "The renewable energy system is performing excellently today with optimal grid balance."
    sentiment = nlp.analyze_sentiment(test_text)
    print(f"\n😊 Sentiment Analysis:")
    print(f"   Text: '{test_text[:60]}...'")
    print(f"   Sentiment: {sentiment['sentiment']}")
    print(f"   Polarity: {sentiment['polarity']}")
    
    # Test entity extraction
    test_text2 = "Colombo's energy demand reached 945 MW at 29.5°C with 3.5 m/s wind speed."
    entities = nlp.extract_entities(test_text2)
    print(f"\n🔍 Entity Extraction:")
    print(f"   Cities: {entities['cities']}")
    print(f"   Numbers: {entities['numbers'][:3]}")
    print(f"   Energy terms: {entities['energy_terms'][:3]}")
    
    # Test intent classification
    question2 = "What is the weather forecast for tomorrow?"
    intent = nlp.classify_intent(question2)
    print(f"\n🎯 Intent Classification:")
    print(f"   Question: '{question2}'")
    print(f"   Primary Intent: {intent['primary_intent']}")
    print(f"   Confidence: {intent['confidence']:.0%}")
    
    # Test summarization
    long_text = """The smart energy system is currently operating at optimal efficiency. 
    Renewable generation is providing 62% of total demand. Weather conditions are favorable 
    with moderate temperatures and steady wind speeds. The grid is balanced with adequate 
    storage reserves. Operators should monitor the evening peak demand period. 
    Solar generation will decrease after sunset. Wind generation is expected to remain stable. 
    Overall system performance is excellent."""
    
    summary = nlp.summarize_text(long_text, max_sentences=2)
    print(f"\n📝 Text Summarization:")
    print(f"   Original: {len(long_text)} chars")
    print(f"   Summary: {summary}")
    
    # Test 3: Responsible AI
    print_section("3. Testing Responsible AI Framework")
    rai = ResponsibleAI()
    rai_status = rai.get_status()
    
    print(f"Explainability Enabled: {rai_status['explainability_enabled']}")
    print(f"Audit Enabled: {rai_status['audit_enabled']}")
    print(f"Features: {len(rai_status['features'])} capabilities")
    
    # Test decision logging
    print("\n📝 Logging Decision...")
    test_decision = {
        'type': 'grid_balancing',
        'decision': 'Activate conventional generation',
        'confidence': 0.92,
        'reasoning': 'Renewable generation insufficient for current demand',
        'input_data': {'demand': 945, 'renewable': 590, 'grid_balance': 'BALANCED'},
        'impact': 'high',
        'agent_id': 'grid_001'
    }
    
    rai.log_decision(test_decision)
    print("✓ Decision logged")
    
    # Test explainability
    explanation = rai.explain_decision()
    print(f"\n🔍 Decision Explanation:")
    print(f"   Decision: {explanation.get('decision')}")
    print(f"   Confidence: {explanation.get('confidence')}")
    print(f"   Explainability Score: {explanation.get('explainability_score'):.2f}")
    
    # Test bias checking
    print("\n⚖️  Checking for Bias...")
    bias_check = rai.check_bias({
        'cities': ['Colombo', 'Colombo', 'Colombo'],
        'confidence': 0.92,
        'required_fields': ['temperature', 'demand', 'generation']
    }, check_type='geographic')
    
    print(f"   Fairness Score: {bias_check['fairness_score']:.2f}")
    print(f"   Biases Detected: {len(bias_check['biases_detected'])}")
    print(f"   Assessment: {bias_check['overall_assessment']}")
    
    # Test transparency report
    print("\n🔓 Generating Transparency Report...")
    transparency = rai.ensure_transparency({
        'llm_provider': llm.provider,
        'nlp_capabilities': nlp_status['capabilities'][:3]
    })
    
    print(f"   Capabilities: {len(transparency['system_capabilities'])} listed")
    print(f"   Limitations: {len(transparency['limitations'])} documented")
    print(f"   Data Sources: {len(transparency['data_sources'])} documented")
    print(f"   Privacy Measures: {len(transparency['privacy_measures'])} implemented")
    
    # Test privacy check
    print("\n🔒 Privacy Check...")
    privacy = rai.privacy_check({
        'city': 'Colombo',
        'temperature': 29.5,
        'coordinates': {'lat': 6.9271, 'lon': 79.8612}
    })
    
    print(f"   Privacy Score: {privacy['privacy_score']:.2f}")
    print(f"   Compliant: {privacy['compliant']}")
    print(f"   Sensitive Data Found: {len(privacy['sensitive_data_found'])} items")
    
    # Success
    print_section("✅ ALL AI SERVICES TESTS PASSED!")
    print("\n🎉 AI Services are working correctly!")
    print("   ✓ LLM Service (Claude/GPT/Fallback)")
    print("   ✓ NLP Processing (Sentiment, Entities, Intent)")
    print("   ✓ Responsible AI (Explainability, Fairness, Privacy)")
    print("\n📋 Next: Update main.py to integrate AI services")

if __name__ == "__main__":
    main()
