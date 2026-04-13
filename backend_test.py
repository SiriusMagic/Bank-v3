import requests
import sys
from datetime import datetime

class AiraCardAPITester:
    def __init__(self, base_url="https://tarjetas-disposables.preview.emergentagent.com"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        self.tests_run = 0
        self.tests_passed = 0
        self.card_ids = []

    def run_test(self, name, method, endpoint, expected_status, data=None, params=None):
        """Run a single API test"""
        url = f"{self.api_url}/{endpoint}"
        headers = {'Content-Type': 'application/json'}

        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        print(f"   URL: {url}")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, params=params, timeout=10)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers, timeout=10)
            elif method == 'PATCH':
                response = requests.patch(url, json=data, headers=headers, timeout=10)

            success = response.status_code == expected_status
            if success:
                self.tests_passed += 1
                print(f"✅ Passed - Status: {response.status_code}")
                try:
                    return success, response.json()
                except:
                    return success, {}
            else:
                print(f"❌ Failed - Expected {expected_status}, got {response.status_code}")
                print(f"   Response: {response.text[:200]}")
                return False, {}

        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            return False, {}

    def test_seed_data(self):
        """Seed the database with test data"""
        print("\n" + "="*60)
        print("SEEDING DATABASE")
        print("="*60)
        success, response = self.run_test(
            "Seed Database",
            "POST",
            "dev/seed",
            200
        )
        if success and 'card_ids' in response:
            self.card_ids = response['card_ids']
            print(f"   Created {len(self.card_ids)} cards")
            return True
        return False

    def test_get_all_cards(self):
        """Test getting all cards"""
        print("\n" + "="*60)
        print("TESTING GET ALL CARDS")
        print("="*60)
        success, response = self.run_test(
            "Get All Cards",
            "GET",
            "cards",
            200
        )
        if success and isinstance(response, list):
            print(f"   Found {len(response)} cards")
            if len(response) > 0:
                self.card_ids = [card['id'] for card in response]
                print(f"   Card IDs: {self.card_ids}")
                # Verify each card has required fields
                for card in response:
                    print(f"\n   Card: {card.get('type', 'unknown')} - Balance: ${card.get('balance', 0)}")
                    print(f"      Frozen: {card.get('frozen', False)}, Cashback: ${card.get('cashback', 0)}")
            return True
        return False

    def test_get_card_details(self, card_id):
        """Test getting specific card details"""
        success, response = self.run_test(
            f"Get Card Details (ID: {card_id[:8]}...)",
            "GET",
            f"cards/{card_id}",
            200
        )
        if success:
            print(f"   Card Type: {response.get('type', 'N/A')}")
            print(f"   Balance: ${response.get('balance', 0)}")
            print(f"   Cashback: ${response.get('cashback', 0)}")
        return success

    def test_get_transactions(self, card_id, range_type="semana"):
        """Test getting transactions for a card"""
        success, response = self.run_test(
            f"Get Transactions ({range_type}) for Card {card_id[:8]}...",
            "GET",
            f"cards/{card_id}/transactions",
            200,
            params={"range": range_type}
        )
        if success and isinstance(response, list):
            print(f"   Found {len(response)} transactions")
            if len(response) > 0:
                print(f"   Sample: {response[0].get('description', 'N/A')} - ${response[0].get('amount', 0)}")
        return success

    def test_get_history(self, card_id, range_type="semana"):
        """Test getting history data for chart"""
        success, response = self.run_test(
            f"Get History ({range_type}) for Card {card_id[:8]}...",
            "GET",
            f"cards/{card_id}/history",
            200,
            params={"range": range_type}
        )
        if success and isinstance(response, list):
            print(f"   Found {len(response)} data points")
            if len(response) > 0:
                print(f"   Sample: {response[0].get('date', 'N/A')} - ${response[0].get('amount', 0)}")
        return success

    def test_get_documents(self, card_id):
        """Test getting documents for a card"""
        success, response = self.run_test(
            f"Get Documents for Card {card_id[:8]}...",
            "GET",
            f"cards/{card_id}/documents",
            200
        )
        if success and isinstance(response, list):
            print(f"   Found {len(response)} documents")
        return success

    def test_freeze_card(self, card_id, freeze_state):
        """Test freezing/unfreezing a card"""
        action = "Freeze" if freeze_state else "Unfreeze"
        success, response = self.run_test(
            f"{action} Card {card_id[:8]}...",
            "PATCH",
            f"cards/{card_id}/freeze",
            200,
            data={"frozen": freeze_state}
        )
        if success:
            print(f"   Card frozen state: {response.get('frozen', 'N/A')}")
        return success

def main():
    print("\n" + "="*60)
    print("AIRA CARD MANAGEMENT SYSTEM - API TESTING")
    print("="*60)
    
    tester = AiraCardAPITester()

    # Step 1: Seed database
    if not tester.test_seed_data():
        print("\n❌ Failed to seed database. Trying to get existing cards...")
        if not tester.test_get_all_cards():
            print("\n❌ No cards available. Cannot continue testing.")
            return 1

    # Step 2: Get all cards
    print("\n" + "="*60)
    print("TESTING CARD RETRIEVAL")
    print("="*60)
    if not tester.test_get_all_cards():
        print("\n❌ Failed to get cards")
        return 1

    if len(tester.card_ids) < 3:
        print(f"\n⚠️  Warning: Expected 3 cards, found {len(tester.card_ids)}")

    # Step 3: Test each card's endpoints
    for i, card_id in enumerate(tester.card_ids[:3]):  # Test first 3 cards
        print("\n" + "="*60)
        print(f"TESTING CARD {i+1} - ID: {card_id[:8]}...")
        print("="*60)
        
        # Get card details
        tester.test_get_card_details(card_id)
        
        # Get transactions for different ranges
        tester.test_get_transactions(card_id, "hoy")
        tester.test_get_transactions(card_id, "semana")
        tester.test_get_transactions(card_id, "personaliza")
        
        # Get history for different ranges
        tester.test_get_history(card_id, "hoy")
        tester.test_get_history(card_id, "semana")
        tester.test_get_history(card_id, "personaliza")
        
        # Get documents
        tester.test_get_documents(card_id)
        
        # Test freeze/unfreeze
        tester.test_freeze_card(card_id, True)
        tester.test_freeze_card(card_id, False)

    # Print summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    print(f"📊 Tests passed: {tester.tests_passed}/{tester.tests_run}")
    print(f"✅ Success rate: {(tester.tests_passed/tester.tests_run*100):.1f}%")
    
    if tester.tests_passed == tester.tests_run:
        print("\n🎉 All tests passed!")
        return 0
    else:
        print(f"\n⚠️  {tester.tests_run - tester.tests_passed} test(s) failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
