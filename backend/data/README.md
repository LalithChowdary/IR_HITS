# Dataset Documentation

## Overview
This directory contains the network datasets used for PageRank and HITS analysis in CSV format.

## File Format
All datasets are stored as **edge lists** in CSV format with the following structure:

```csv
source,target
Node1,Node2
Node3,Node4
...
```

- **source**: The node from which the edge originates (citing paper, mentioning user, etc.)
- **target**: The node to which the edge points (cited paper, mentioned user, etc.)
- Each row represents a directed edge in the network

## Datasets

### 1. Citation Network (`citation_network.csv`)
**Domain**: Academic Paper Citations  
**Nodes**: 15 research papers (Paper_A through Paper_O)  
**Edges**: 24 citation relationships  
**Description**: Represents papers citing each other in academic research

**Network Characteristics**:
- Seminal papers (Paper_A, Paper_B, Paper_C) are frequently cited
- Recent papers cite earlier influential work
- Creates a hierarchical citation structure

**Example edges**:
```csv
source,target
Paper_D,Paper_A  # Paper D cites Paper A
Paper_M,Paper_E  # Paper M cites Paper E
```

### 2. Social Network (`social_network.csv`)
**Domain**: Social Media Interactions  
**Nodes**: 15 users (User_1 through User_15)  
**Edges**: 30 mention/retweet relationships  
**Description**: Represents users mentioning or retweeting each other

**Network Characteristics**:
- Influencers (User_1, User_2, User_3) are mentioned frequently
- Some users act as hubs (User_15, User_11) by mentioning many others
- Includes reciprocal mentions creating network cycles

**Example edges**:
```csv
source,target
User_4,User_1  # User 4 mentions User 1
User_15,User_2 # User 15 retweets User 2
```

## Usage

### Loading in Python
```python
import csv

edges = []
nodes = set()

with open('citation_network.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        source = row['source']
        target = row['target']
        edges.append((source, target))
        nodes.add(source)
        nodes.add(target)

print(f"Nodes: {len(nodes)}")
print(f"Edges: {len(edges)}")
```

### Via API
```bash
# Get dataset information
curl http://127.0.0.1:8000/api/dataset/citation
curl http://127.0.0.1:8000/api/dataset/social

# Get network statistics
curl http://127.0.0.1:8000/api/network/citation
curl http://127.0.0.1:8000/api/network/social
```

## Dataset Statistics

### Citation Network
- **Nodes**: 15
- **Edges**: 24
- **Density**: 0.114 (11.4% of possible edges exist)
- **Average Degree**: 3.2

### Social Network
- **Nodes**: 15
- **Edges**: 30
- **Density**: 0.143 (14.3% of possible edges exist)
- **Average Degree**: 4.0

## Creating Custom Datasets

To add a new network:

1. Create a CSV file with `source,target` header
2. Add directed edges (one per line)
3. Save in the `data/` directory
4. Update `sample_networks.py` to load the new network

**Example**:
```csv
source,target
Website1,Website2
Website1,Website3
Website2,Website4
Website3,Website1
```

## Notes

- All edges are **directed** (source → target)
- Node names should not contain commas
- The CSV files are automatically loaded by the API on startup
- Networks should have 10-20 nodes for optimal visualization
