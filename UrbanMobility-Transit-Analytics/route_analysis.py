import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import os

# Load bus routes
df = pd.read_csv(
    "UrbanMobility-Transit-Analytics/outputs/cleaned_da_bus_routes.csv"
)

# Create graph
G = nx.Graph()

for _, row in df.iterrows():
    G.add_edge(
        row["start_stop"],
        row["end_stop"],
        route_id=row["route_id"]
    )

# Print results
print("Total bus routes:", len(df))
print("Total unique stops:", G.number_of_nodes())
print("Total connections:", G.number_of_edges())
print("Connected network:", nx.is_connected(G))

# Draw graph
plt.figure(figsize=(16, 10))

pos = nx.spring_layout(G, seed=42, k=1.2)

nx.draw_networkx_nodes(
    G, pos, node_size=650, node_color="black"
)

nx.draw_networkx_edges(
    G, pos, edge_color="teal", width=2
)

nx.draw_networkx_labels(
    G, pos, font_size=8, font_color="darkblue"
)

plt.title("UrbanMobility Transit Analytics - Bus Route Network")
plt.axis("off")
plt.tight_layout()

# Save image
os.makedirs("UrbanMobility-Transit-Analytics/outputs", exist_ok=True)

plt.savefig(
    "UrbanMobility-Transit-Analytics/outputs/route_network.png",
    dpi=300,
    bbox_inches="tight"
)

print("Graph image saved as outputs/route_network.png")

# Display image
plt.show()