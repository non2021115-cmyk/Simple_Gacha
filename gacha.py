import random
import datetime
import hashlib

class GachaSystem:
    def __init__(self):
        # Random seeds for each unique value
        self.pickup_value_unique_seed = []
        
        # Rank weights (probability distribution for ranks)
        self.weight1 = []
        
        # Value weights for each rank (probability distribution for values within rank)
        self.weight2 = {}
        
        # Available ranks
        self.rank = []
        
        # Values for each rank
        self.value_by_rank = {}
    
    def setup(self, ranks_config):
        """
        Setup gacha system with rank and value configurations
        
        ranks_config format:
        {
            'SSR': {'weight': 0.02, 'values': ['char1', 'char2'], 'weights': [0.5, 0.5]},
            'SR': {'weight': 0.15, 'values': ['char3', 'char4'], 'weights': [0.6, 0.4]},
            'R': {'weight': 0.83, 'values': ['char5', 'char6'], 'weights': [0.5, 0.5]}
        }
        """
        self.rank = []
        self.weight1 = []
        self.weight2 = {}
        self.value_by_rank = {}
        
        for rank_name, config in ranks_config.items():
            self.rank.append(rank_name)
            self.weight1.append(config['weight'])
            self.weight2[rank_name] = config['weights']
            self.value_by_rank[rank_name] = config['values']
            
            # Generate unique seeds for each value
            for value in config['values']:
                seed_str = f"{rank_name}_{value}_{len(self.pickup_value_unique_seed)}"
                seed = int(hashlib.md5(seed_str.encode()).hexdigest(), 16)
                self.pickup_value_unique_seed.append(seed)
    
    def generate_seed(self, unique_id=None):
        """
        Generate random seed from date + time + unique_id
        """
        now = datetime.datetime.now()
        timestamp = now.strftime("%Y%m%d%H%M%S%f")
        
        seed_components = [timestamp]
        if unique_id:
            seed_components.append(str(unique_id))
        
        seed_str = ''.join(seed_components)
        seed = int(hashlib.md5(seed_str.encode()).hexdigest(), 16)
        
        return seed
    
    def pull(self, user_id=None):
        """
        Perform a single gacha pull
        Returns: (rank, value)
        """
        # Generate seed
        seed = self.generate_seed(user_id)
        random.seed(seed)
        
        # Step 1: Select rank according to weight1
        selected_rank = random.choices(self.rank, weights=self.weight1, k=1)[0]
        
        # Step 2: Select value from selected rank by weight2
        values_in_rank = self.value_by_rank[selected_rank]
        weights_for_rank = self.weight2[selected_rank]
        selected_value = random.choices(values_in_rank, weights=weights_for_rank, k=1)[0]
        
        return selected_rank, selected_value
    
    def pull_multiple(self, count=10, user_id=None):
        """
        Perform multiple gacha pulls
        Returns: list of (rank, value) tuples
        """
        results = []
        for i in range(count):
            # Modify seed for each pull
            pull_seed = self.generate_seed(f"{user_id}_{i}" if user_id else i)
            random.seed(pull_seed)
            
            selected_rank = random.choices(self.rank, weights=self.weight1, k=1)[0]
            values_in_rank = self.value_by_rank[selected_rank]
            weights_for_rank = self.weight2[selected_rank]
            selected_value = random.choices(values_in_rank, weights=weights_for_rank, k=1)[0]
            
            results.append((selected_rank, selected_value))
        
        return results


# Example usage
if __name__ == "__main__":
    gacha = GachaSystem()
    
    # Setup gacha rates and values
    config = {
        'SSR': {
            'weight': 0.02,
            'values': ['Legend_Character_1', 'Legend_Character_2'],
            'weights': [0.5, 0.5]
        },
        'SR': {
            'weight': 0.15,
            'values': ['Rare_Character_1', 'Rare_Character_2', 'Rare_Character_3'],
            'weights': [0.4, 0.3, 0.3]
        },
        'R': {
            'weight': 0.83,
            'values': ['Common_Character_1', 'Common_Character_2'],
            'weights': [0.6, 0.4]
        }
    }
    
    gacha.setup(config)
    
    # Single pull
    rank, value = gacha.pull(user_id="player_123")
    print(f"Single Pull: {rank} - {value}")
    
    # Multiple pulls
    print("\n10-Pull Results:")
    results = gacha.pull_multiple(count=10, user_id="player_123")
    for i, (rank, value) in enumerate(results, 1):
        print(f"  {i}. {rank} - {value}")
    
    # Statistics
    print("\nStatistics from 1000 pulls:")
    all_results = gacha.pull_multiple(count=1000, user_id="player_stats")
    rank_counts = {}
    for rank, _ in all_results:
        rank_counts[rank] = rank_counts.get(rank, 0) + 1
    
    for rank in gacha.rank:
        percentage = (rank_counts.get(rank, 0) / 1000) * 100
        print(f"  {rank}: {percentage:.2f}%")