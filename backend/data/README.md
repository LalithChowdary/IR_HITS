# Dataset Documentation

## Overview
This directory contains the citation network dataset used for PageRank and HITS analysis in CSV format.

## File Format
The dataset is stored as an **edge list** in CSV format with the following structure:

```csv
source,target
Node1,Node2
Node3,Node4
...
```

- **source**: The node from which the edge originates (citing paper)
- **target**: The node to which the edge points (cited paper)
- Each row represents a directed edge in the network

## Dataset

### Citation Network (`citation_network.csv`)
**Domain**: Academic Paper Citations  
**Format**: Edge list (source → target)  
**Description**: Represents papers citing each other in academic research

**Example edges**:
```csv
source,target
5,6  # Paper 5 cites Paper 6
2,3  # Paper 2 cites Paper 3
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
curl http://127.0.0.1:8000/api/dataset

# Get network statistics
curl http://127.0.0.1:8000/api/network
```

## Modifying the Dataset

To update the citation network:

1. Edit `citation_network.csv` with your edge data
2. Keep the format: `source,target` (use **commas**, not spaces)
3. The backend will automatically reload the changes
4. Verify with: `curl http://127.0.0.1:8000/api/network`

**Example**:
```csv
source,target
1,2
1,3
2,4
3,4
```

## Notes

- All edges are **directed** (source → target)
- Node names should not contain commas
- The CSV file is automatically loaded by the backend on startup
- Changes to the CSV require backend restart to take effect

