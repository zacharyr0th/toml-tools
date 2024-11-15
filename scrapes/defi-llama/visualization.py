import matplotlib.pyplot as plt
import pandas as pd
import os
from datetime import datetime
import logging
import seaborn as sns
import numpy as np
from matplotlib.ticker import FuncFormatter
from concurrent.futures import ThreadPoolExecutor

# Set the style - using updated style name
plt.style.use('seaborn-v0_8-darkgrid')

# Configure plot settings
plt.rcParams['figure.figsize'] = (15, 10)
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['xtick.labelsize'] = 10
plt.rcParams['ytick.labelsize'] = 10

# Set Matplotlib to use a non-interactive backend and configure for performance
plt.switch_backend('agg')
plt.rcParams['path.simplify'] = True
plt.rcParams['path.simplify_threshold'] = 1.0
plt.rcParams['agg.path.chunksize'] = 10000

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def format_large_number(num):
    """Format large numbers to human-readable format"""
    if num >= 1e9:
        return f'${num/1e9:.1f}B'
    elif num >= 1e6:
        return f'${num/1e6:.1f}M'
    elif num >= 1e3:
        return f'${num/1e3:.1f}K'
    return f'${num:.0f}'

def save_plot(plt, viz_dir, filename):
    """Save plot with error handling"""
    try:
        output_path = os.path.join(viz_dir, filename)
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        logger.info(f"Saved: {output_path}")
    except Exception as e:
        logger.error(f"Error saving plot {filename}: {str(e)}")
    finally:
        plt.close()

def generate_protocol_visualizations(protocols, viz_dir, current_date):
    """Generate visualizations for protocols"""
    logger.info("Generating protocol visualizations...")

    # Top Protocols by TVL
    plt.figure(figsize=(20, 10))
    top_protocols = protocols.nlargest(10, 'tvl')
    bars = plt.barh(top_protocols['name'], top_protocols['tvl'])
    plt.title('Top 10 Protocols by TVL', pad=20, fontweight='bold')
    plt.xlabel('TVL (USD)', fontweight='bold')
    for bar in bars:
        width = bar.get_width()
        plt.text(width, bar.get_y() + bar.get_height()/2, format_large_number(width), ha='left', va='center')
    save_plot(plt, viz_dir, f'top_protocols_tvl_{current_date}.png')

    # Protocol Categories
    if 'category' in protocols.columns:
        plt.figure(figsize=(15, 10))
        category_counts = protocols['category'].value_counts()
        plt.pie(category_counts.values, labels=[f'{cat}\n({count})' for cat, count in category_counts.items()], autopct='%1.1f%%')
        plt.title('Distribution of Protocol Categories', pad=20, fontweight='bold')
        save_plot(plt, viz_dir, f'protocol_categories_{current_date}.png')

    # Chain Distribution
    if 'chain' in protocols.columns:
        plt.figure(figsize=(15, 10))
        chain_tvl = protocols.groupby('chain')['tvl'].sum().sort_values(ascending=False)
        significant_chains = chain_tvl[chain_tvl/chain_tvl.sum() > 0.01]
        plt.pie(significant_chains, labels=[f'{chain}\n({format_large_number(tvl)})' for chain, tvl in significant_chains.items()], autopct='%1.1f%%', startangle=90)
        plt.title('TVL Distribution by Chain', pad=20, fontweight='bold')
        plt.axis('equal')
        save_plot(plt, viz_dir, f'chain_tvl_pie_{current_date}.png')

    # Audit Distribution
    if 'audits' in protocols.columns:
        logger.info("Generating audit distribution visualization...")
        plt.figure(figsize=(12, 8))
        audit_counts = protocols['audits'].value_counts().sort_index()
        bars = plt.bar(audit_counts.index.astype(str), audit_counts.values, color='skyblue', edgecolor='black')
        plt.title('Distribution of Protocol Audit Counts', pad=20, fontweight='bold')
        plt.xlabel('Number of Audits', fontweight='bold')
        plt.ylabel('Number of Protocols', fontweight='bold')
        
        # Add value labels on top of each bar
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                     f'{height}',
                     ha='center', va='bottom')
        
        # Add a text box with summary statistics
        total_protocols = len(protocols)
        audited_protocols = len(protocols[protocols['audits'] > 0])
        avg_audits = protocols['audits'].mean()
        
        stats_text = f"Total Protocols: {total_protocols}\n"
        stats_text += f"Audited Protocols: {audited_protocols} ({audited_protocols/total_protocols:.1%})\n"
        stats_text += f"Average Audits per Protocol: {avg_audits:.2f}"
        
        plt.text(0.95, 0.95, stats_text, transform=plt.gca().transAxes, fontsize=10,
                 verticalalignment='top', horizontalalignment='right',
                 bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        
        plt.tight_layout()
        save_plot(plt, viz_dir, f'audit_distribution_{current_date}.png')

    # Protocol Launch Timeline
    if 'listedAt' in protocols.columns:
        plt.figure(figsize=(15, 8))
        launch_dates = pd.to_datetime(protocols['listedAt'], unit='s')
        plt.hist(launch_dates, bins=30, edgecolor='black')
        plt.title('Protocol Launch Timeline', pad=20, fontweight='bold')
        plt.xlabel('Launch Date', fontweight='bold')
        plt.ylabel('Number of Protocols', fontweight='bold')
        plt.xticks(rotation=45)
        plt.tight_layout()
        save_plot(plt, viz_dir, f'protocol_launches_{current_date}.png')

    # TVL Change Analysis
    if 'change_1d' in protocols.columns and 'change_7d' in protocols.columns:
        plt.figure(figsize=(15, 10))
        
        # Create box plots for 1d and 7d changes
        change_data = [
            protocols['change_1d'].dropna(),
            protocols['change_7d'].dropna()
        ]
        
        bp = plt.boxplot(change_data, labels=['24h Change', '7d Change'])
        plt.title('TVL Changes Distribution', pad=20, fontweight='bold')
        plt.ylabel('Percentage Change (%)', fontweight='bold')
        
        # Add mean values as text
        for i, changes in enumerate(change_data, 1):
            mean_val = changes.mean()
            plt.text(i, plt.ylim()[0], f'Mean: {mean_val:.2f}%', 
                    horizontalalignment='center', verticalalignment='top')
        
        save_plot(plt, viz_dir, f'tvl_changes_{current_date}.png')

    # Protocol Age vs TVL
    if 'listedAt' in protocols.columns:
        plt.figure(figsize=(15, 10))
        current_timestamp = datetime.now().timestamp()
        protocols['age_days'] = (current_timestamp - protocols['listedAt']) / (24 * 3600)
        
        plt.scatter(protocols['age_days'], protocols['tvl'], alpha=0.5)
        plt.xscale('log')
        plt.yscale('log')
        plt.title('Protocol Age vs TVL', pad=20, fontweight='bold')
        plt.xlabel('Age (Days)', fontweight='bold')
        plt.ylabel('TVL (USD)', fontweight='bold')
        
        # Add correlation coefficient
        correlation = protocols['age_days'].corr(protocols['tvl'])
        plt.text(0.95, 0.95, f'Correlation: {correlation:.2f}', 
                transform=plt.gca().transAxes, 
                bbox=dict(facecolor='white', alpha=0.8))
        
        save_plot(plt, viz_dir, f'age_vs_tvl_{current_date}.png')

    # Monthly Protocol Growth
    if 'listedAt' in protocols.columns:
        plt.figure(figsize=(15, 8))
        launch_dates = pd.to_datetime(protocols['listedAt'], unit='s')
        monthly_counts = launch_dates.groupby(pd.Grouper(freq='M')).size()
        
        plt.plot(monthly_counts.index, monthly_counts.values.cumsum(), marker='o')
        plt.title('Cumulative Protocol Growth Over Time', pad=20, fontweight='bold')
        plt.xlabel('Date', fontweight='bold')
        plt.ylabel('Total Number of Protocols', fontweight='bold')
        plt.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        
        save_plot(plt, viz_dir, f'protocol_growth_{current_date}.png')

    # TVL Distribution Analysis
    plt.figure(figsize=(15, 8))
    tvl_data = protocols['tvl'].dropna()
    
    # Create histogram with density plot
    sns.histplot(data=tvl_data, x='tvl', bins=50, stat='density', alpha=0.5)
    sns.kdeplot(data=tvl_data, x='tvl', color='red')
    
    plt.title('TVL Distribution Across Protocols', pad=20, fontweight='bold')
    plt.xlabel('TVL (USD)', fontweight='bold')
    plt.ylabel('Density', fontweight='bold')
    plt.xscale('log')
    
    # Add summary statistics
    stats_text = f"Mean TVL: {format_large_number(tvl_data.mean())}\n"
    stats_text += f"Median TVL: {format_large_number(tvl_data.median())}\n"
    stats_text += f"Std Dev: {format_large_number(tvl_data.std())}"
    
    plt.text(0.95, 0.95, stats_text, transform=plt.gca().transAxes,
             bbox=dict(facecolor='white', alpha=0.8),
             verticalalignment='top', horizontalalignment='right')
    
    save_plot(plt, viz_dir, f'tvl_distribution_{current_date}.png')

def generate_dex_visualizations(dex_data, viz_dir, current_date):
    """Generate visualizations for DEXes"""
    if not dex_data.empty:
        logger.info("Generating DEX visualizations...")
        plt.figure(figsize=(20, 10))
        top_dexes = dex_data.nlargest(15, 'dailyVolume')
        bars = plt.barh(top_dexes['name'], top_dexes['dailyVolume'])
        plt.title('Top 15 DEXes by Daily Trading Volume', pad=20, fontweight='bold')
        plt.xlabel('Daily Volume (USD)', fontweight='bold')
        for bar in bars:
            width = bar.get_width()
            plt.text(width, bar.get_y() + bar.get_height()/2, format_large_number(width), ha='left', va='center')
        save_plot(plt, viz_dir, f'top_dexes_volume_{current_date}.png')

def generate_yields_visualizations(yields_data, viz_dir, current_date):
    """Generate visualizations for yields"""
    if not yields_data.empty:
        logger.info("Generating yields visualizations...")
        
        # Top Pools by APY
        plt.figure(figsize=(20, 10))
        top_pools = yields_data.nlargest(20, 'apy')
        bars = plt.barh(top_pools['pool'], top_pools['apy'])
        plt.title('Top 20 Pools by APY', pad=20, fontweight='bold')
        plt.xlabel('APY (%)', fontweight='bold')
        for bar in bars:
            width = bar.get_width()
            plt.text(width, bar.get_y() + bar.get_height()/2, f'{width:.1f}%', ha='left', va='center')
        save_plot(plt, viz_dir, f'top_pools_apy_{current_date}.png')

        # APY vs TVL scatter plot
        plt.figure(figsize=(15, 10))
        plt.scatter(yields_data['tvlUsd'], yields_data['apy'], alpha=0.6, s=100)
        plt.xscale('log')
        plt.yscale('log')
        plt.xlabel('TVL (USD)', fontweight='bold')
        plt.ylabel('APY (%)', fontweight='bold')
        plt.title('Yield Pools: APY vs TVL Distribution', pad=20, fontweight='bold')
        plt.grid(True, alpha=0.3)
        save_plot(plt, viz_dir, f'yield_apy_vs_tvl_{current_date}.png')

def generate_visualizations(protocols, dex_data, yields_data, output_dir):
    """Generate comprehensive visualizations from DeFi Llama data."""
    try:
        viz_dir = os.path.join(output_dir, "visualizations")
        os.makedirs(viz_dir, exist_ok=True)
        current_date = datetime.now().strftime('%Y-%m-%d')
        logger.info(f"Saving visualizations to: {viz_dir}")

        with ThreadPoolExecutor() as executor:
            executor.submit(generate_protocol_visualizations, protocols, viz_dir, current_date)
            executor.submit(generate_dex_visualizations, dex_data, viz_dir, current_date)
            executor.submit(generate_yields_visualizations, yields_data, viz_dir, current_date)

    except Exception as e:
        logger.error(f"Fatal error in visualization generation: {str(e)}")
        raise

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python3 visualization.py <ecosystem>")
        print("Example: python3 visualization.py aptos")
        sys.exit(1)

    ecosystem = sys.argv[1]
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(current_dir))
    data_dir = os.path.join(project_root, "output", f"{ecosystem}-defi-llama-data")
    logger.info(f"Looking for data in: {data_dir}")

    if not os.path.exists(data_dir):
        logger.error(f"Directory not found: {data_dir}")
        logger.error(f"Make sure the directory '{ecosystem}-defi-llama-data' exists in the output folder")
        sys.exit(1)

    try:
        protocol_files = [f for f in os.listdir(data_dir) if f.startswith('protocols-') and f.endswith('.csv')]
        if not protocol_files:
            logger.error(f"No protocol files found in {data_dir}")
            sys.exit(1)

        dates = [f.replace('protocols-', '').replace('.csv', '') for f in protocol_files]
        most_recent_date = max(dates)
        protocols_path = os.path.join(data_dir, f"protocols-{most_recent_date}.csv")
        dex_path = os.path.join(data_dir, f"dexes-{most_recent_date}.csv")
        yields_path = os.path.join(data_dir, f"yields-{most_recent_date}.csv")
        logger.info(f"Using data files from: {most_recent_date}")

        protocols = pd.read_csv(protocols_path) if os.path.getsize(protocols_path) > 0 else pd.DataFrame()
        dex_data = pd.read_csv(dex_path) if os.path.getsize(dex_path) > 0 else pd.DataFrame()
        yields_data = pd.read_csv(yields_path) if os.path.getsize(yields_path) > 0 else pd.DataFrame()

        if protocols.empty and dex_data.empty and yields_data.empty:
            logger.error("All data files are empty. Cannot generate visualizations.")
            sys.exit(1)

        generate_visualizations(protocols, dex_data, yields_data, data_dir)
    except Exception as e:
        logger.error(f"Error loading data files: {str(e)}")
        sys.exit(1)