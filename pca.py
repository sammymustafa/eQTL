from setup import *

### COMPELTE HERE ###
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from io import StringIO

data_string = eqtl_data["ExpData.txt"].decode('utf-8')

# Convert the string to a file-like object
data_file = StringIO(data_string)

# Read the data into a pandas DataFrame
df = pd.read_csv(data_file, sep='\t')

# Drop the first column if it's not part of the expression data
# Assuming the first column is 'Patient' or similar, which is not part of the expression data
X = df.drop(columns=df.columns[0])

# Standardize the data
scaler = StandardScaler()
X_std = scaler.fit_transform(X)

# Perform PCA
pca = PCA(n_components=2)  # Adjust the number of components as necessary
X_pca = pca.fit_transform(X_std)

# Perform k-means clustering
kmeans = KMeans(n_clusters=2)  # Adjust the number of clusters as necessary
X_clustered = kmeans.fit_predict(X_std)

# Plotting the PCA result
plt.figure(figsize=(8, 6))
scatter = plt.scatter(X_pca[:, 0], X_pca[:, 1], c=X_clustered, cmap='viridis')

# Set x-axis ticks to three concrete numbers. Adjust the numbers as per your requirement.
plt.xticks([-5, 0, 5])

plt.title('PCA of Gene Expression Data')
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')

# Create a legend for the clusters:
# Find the unique clusters and their colors from the scatter plot
unique_clusters = np.unique(X_clustered)
colors = [scatter.cmap(scatter.norm(cluster)) for cluster in unique_clusters]

# Create custom legend entries
import matplotlib.patches as mpatches
legend_handles = [mpatches.Patch(color=colors[i], label=f'Cluster {unique_clusters[i]}') for i in range(len(unique_clusters))]

# Add the custom legend to the plot
plt.legend(handles=legend_handles, title='Sub-population Cluster')

plt.show()