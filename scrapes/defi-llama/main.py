import requests
import pandas as pd
from datetime import datetime
import os
import time
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import matplotlib.pyplot as plt
import numpy as np
from visualization import generate_visualizations

# Set Matplotlib to use a non-interactive backend and configure for performance
plt.switch_backend('agg')
plt.rcParams['path.simplify'] = True
plt.rcParams['path.simplify_threshold'] = 1.0
plt.rcParams['agg.path.chunksize'] = 10000

class ChainDataFetcher:
    BASE_URL = "https://api.llama.fi"

    def __init__(self, chains):
        """
        Initialize with a list of chains to fetch data for
        chains: list of chain names (e.g., ['Solana', 'Ethereum'])
        """
        self.chains = [chain.capitalize() for chain in chains]  # Normalize chain names
        self.session = requests.Session()
        retries = Retry(total=5, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
        self.session.mount('https://', HTTPAdapter(max_retries=retries))

    def _make_request(self, endpoint, params=None):
        response = None
        try:
            response = self.session.get(f"{self.BASE_URL}{endpoint}", params=params, timeout=60)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error making request to {endpoint}: {str(e)}")
            print(f"Response content: {response.text if response else 'No response'}")
            return None

    def get_protocols(self):
        """Get protocols for specified chains"""
        protocols = self._make_request("/protocols")
        if protocols:
            df = pd.DataFrame(protocols)
            chain_protocols = df[df['chain'].isin(self.chains)]
            return chain_protocols
        return pd.DataFrame()

    def get_protocol_details(self, protocol_slug):
        """Get detailed protocol information including TVL breakdowns"""
        data = self._make_request(f"/protocol/{protocol_slug}")
        if data:
            return pd.DataFrame([data])
        return pd.DataFrame()

    def get_yields(self):
        """Get yield pools data for specified chains"""
        pools = self._make_request("/pools")
        if pools:
            df = pd.DataFrame(pools)
            chain_pools = df[df['chain'].isin(self.chains)]
            return chain_pools
        return pd.DataFrame()

    def get_dexes(self):
        """Get DEX data for specified chains"""
        params = {
            'excludeTotalDataChart': 'true',
            'excludeTotalDataChartBreakdown': 'true',
            'dataType': 'dailyVolume'
        }
        data = self._make_request("/overview/dexs", params=params)
        if data and isinstance(data, dict) and 'protocols' in data:
            chain_dexes = [dex for dex in data['protocols'] if dex.get('chain') in self.chains]
            return pd.DataFrame(chain_dexes)
        return pd.DataFrame()

    def get_fees(self):
        """Get fees data for specified chains"""
        params = {
            'excludeTotalDataChart': 'true',
            'excludeTotalDataChartBreakdown': 'true',
            'dataType': 'dailyFees'
        }
        data = self._make_request("/overview/fees", params=params)
        if data and isinstance(data, dict) and 'protocols' in data:
            chain_fees = [fee for fee in data['protocols'] if fee.get('chain') in self.chains]
            return pd.DataFrame(chain_fees)
        return pd.DataFrame()

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Fetch DeFi data for specified blockchain ecosystems')
    parser.add_argument('chains', nargs='+', help='List of chains to fetch data for (e.g., solana ethereum)')
    parser.add_argument('--output-dir', default='output', 
                       help='Directory to store output files')
    args = parser.parse_args()

    # Get the absolute path of the script's directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Resolve output path relative to script directory
    output_base = os.path.abspath(os.path.join(script_dir, '..', '..', args.output_dir))
    
    current_date = datetime.now().strftime("%Y-%m-%d")
    is_single_chain = len(args.chains) == 1
    
    chains_str = args.chains[0].lower() if is_single_chain else '-'.join(sorted(args.chains))
    
    if is_single_chain:
        # For single chain, use simpler directory structure
        output_dir = os.path.join(output_base, f"{args.chains[0].lower()}-defi-llama-data")
    else:
        # For multiple chains, use combined directory structure
        output_dir = os.path.join(output_base, f"{chains_str}-defi-llama-data")
    
    os.makedirs(output_dir, exist_ok=True)
    
    # Create subdirectories for each chain
    chain_dirs = {}
    for chain in args.chains:
        chain_dir = os.path.join(output_dir, chain.lower())
        os.makedirs(chain_dir, exist_ok=True)
        chain_dirs[chain.lower()] = chain_dir
    
    print(f"Using absolute output path: {output_dir}")
    
    fetcher = ChainDataFetcher(args.chains)
    
    data_summary = {
        'date': current_date,
        'chains': chains_str
    }

    print(f"Fetching data for chains: {', '.join(args.chains)}")
    
    print("Fetching protocols...")
    protocols = fetcher.get_protocols()
    if not protocols.empty:
        # Save protocols for each chain
        for chain in args.chains:
            chain_protocols = protocols[protocols['chain'].str.lower() == chain.lower()]
            if not chain_protocols.empty:
                chain_protocols.to_csv(f"{chain_dirs[chain.lower()]}/protocols-{current_date}.csv", index=False)
        
        # Save combined protocols only for multiple chains
        if not is_single_chain:
            protocols.to_csv(f"{output_dir}/protocols-combined-{current_date}.csv", index=False)
        data_summary['total_protocols'] = len(protocols)
        
        print("Fetching detailed protocol information...")
        all_protocol_details = []
        chain_protocol_details = {chain.lower(): [] for chain in args.chains}
        
        for protocol in protocols['slug'].unique():
            print(f"Getting details for {protocol}...")
            details = fetcher.get_protocol_details(protocol)
            if not details.empty:
                all_protocol_details.append(details)
                # Sort protocol details into chain-specific lists
                protocol_chain = details['chain'].iloc[0].lower()
                if protocol_chain in chain_dirs:
                    chain_protocol_details[protocol_chain].append(details)
            time.sleep(1)
        
        # Save protocol details for each chain
        for chain in args.chains:
            if chain_protocol_details[chain.lower()]:
                chain_details = pd.concat(chain_protocol_details[chain.lower()], ignore_index=True)
                chain_details.to_csv(f"{chain_dirs[chain.lower()]}/protocol-details-{current_date}.csv", index=False)
        
        # Save combined details
        if all_protocol_details:
            combined_details = pd.concat(all_protocol_details, ignore_index=True)
            combined_details.to_csv(f"{output_dir}/protocol-details-combined-{current_date}.csv", index=False)

    print("Fetching yields data...")
    yields_data = fetcher.get_yields()
    if not yields_data.empty:
        # Save yields for each chain
        for chain in args.chains:
            chain_yields = yields_data[yields_data['chain'].str.lower() == chain.lower()]
            if not chain_yields.empty:
                chain_yields.to_csv(f"{chain_dirs[chain.lower()]}/yields-{current_date}.csv", index=False)
        # Save combined yields
        yields_data.to_csv(f"{output_dir}/yields-combined-{current_date}.csv", index=False)
        data_summary['total_yield_pools'] = len(yields_data)

    print("Fetching DEX data...")
    dex_data = fetcher.get_dexes()
    if not dex_data.empty:
        # Save DEX data for each chain
        for chain in args.chains:
            chain_dexes = dex_data[dex_data['chain'].str.lower() == chain.lower()]
            if not chain_dexes.empty:
                chain_dexes.to_csv(f"{chain_dirs[chain.lower()]}/dexes-{current_date}.csv", index=False)
        # Save combined DEX data
        dex_data.to_csv(f"{output_dir}/dexes-combined-{current_date}.csv", index=False)
        data_summary['total_dexes'] = len(dex_data)

    print("Fetching fees data...")
    fees_data = fetcher.get_fees()
    if not fees_data.empty:
        # Save fees data for each chain
        for chain in args.chains:
            chain_fees = fees_data[fees_data['chain'].str.lower() == chain.lower()]
            if not chain_fees.empty:
                chain_fees.to_csv(f"{chain_dirs[chain.lower()]}/fees-{current_date}.csv", index=False)
        # Save combined fees data
        fees_data.to_csv(f"{output_dir}/fees-combined-{current_date}.csv", index=False)
        data_summary['total_fees_entries'] = len(fees_data)

    # Save summary for each chain and combined
    for chain in args.chains:
        chain_summary = {k: v for k, v in data_summary.items()}
        chain_summary['chain'] = chain.lower()
        pd.DataFrame([chain_summary]).to_csv(f"{chain_dirs[chain.lower()]}/summary-{current_date}.csv", index=False)
    
    summary_df = pd.DataFrame([data_summary])
    summary_df.to_csv(f"{output_dir}/summary-combined-{current_date}.csv", index=False)

    print("\nData Collection Summary:")
    for key, value in data_summary.items():
        print(f"{key}: {value}")
    
    print(f"\nAll data has been saved to: {output_dir}")

    # Generate visualizations for each chain
    print("\nGenerating visualizations...")
    for chain in args.chains:
        print(f"Generating visualizations for {chain}...")
        chain_protocols = protocols[protocols['chain'].str.lower() == chain.lower()] if not protocols.empty else pd.DataFrame()
        chain_dexes = dex_data[dex_data['chain'].str.lower() == chain.lower()] if not dex_data.empty else pd.DataFrame()
        chain_yields = yields_data[yields_data['chain'].str.lower() == chain.lower()] if not yields_data.empty else pd.DataFrame()
        
        generate_visualizations(
            protocols=chain_protocols,
            dex_data=chain_dexes,
            yields_data=chain_yields,
            output_dir=chain_dirs[chain.lower()]
        )

    # Generate combined visualizations
    if not is_single_chain:
        print("Generating combined visualizations...")
        generate_visualizations(
            protocols=protocols,
            dex_data=dex_data,
            yields_data=yields_data,
            output_dir=output_dir
        )

if __name__ == "__main__":
    main()