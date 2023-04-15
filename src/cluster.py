import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib as mpl
from math import pi
import streamlit as st
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans, DBSCAN
from yellowbrick.cluster import KElbowVisualizer
from sklearn.metrics import silhouette_score
from sklearn.metrics import davies_bouldin_score
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import seaborn as sns
from mpl_toolkits import mplot3d
from ds_utils.unsupervised import plot_cluster_cardinality, plot_cluster_magnitude, plot_magnitude_vs_cardinality
from scipy.spatial.distance import euclidean


def boxplots_df(df_num):    
    # create the figure for the subplots
    fig, ax = plt.subplots(len(df_num.columns), 1, figsize=(30,30))
    
    # Create a boxplot for every numerica columns
    for i in range(len(df_num.columns)):
        sns.boxplot(x=df_num.columns[i], data=df_num, ax=ax[i], color = "teal")
    plt.show()

def standarscaler(df_num, features):
    sc = StandardScaler()
    scaled = pd.DataFrame(sc.fit_transform(df_num))
    scaled.columns = features
    return scaled


def inertia_silhouette_db(df_scaled):
    inertia = []
    silhouette = []
    db_scores = []
    for k in range(2, 11):
        kmeans = KMeans(n_clusters=k, random_state=42)
        kmeans.fit(df_scaled)
        inertia.append(kmeans.inertia_)
        silhouette.append(silhouette_score(df_scaled, kmeans.predict(df_scaled)))
        db_scores.append(davies_bouldin_score(df_scaled, kmeans.labels_))

    # Plot inertia, silhouette, and Davies-Bouldin index
    fig, axs = plt.subplots(1, 3, figsize=(16, 4))
    axs[0].plot(range(2, 11), inertia, 'bx-', color="yellow")
    axs[0].set_xlabel('Number of clusters (k)')
    axs[0].set_ylabel('Inertia')
    axs[0].set_title('Elbow Method')

    axs[1].plot(range(2, 11), silhouette, 'bx-', color= "green")
    axs[1].set_xlabel('Number of clusters (k)')
    axs[1].set_ylabel('Silhouette')
    axs[1].set_title('Silhouette Method')

    axs[2].plot(range(2, 11), db_scores, 'bx-', color= "blue")
    axs[2].set_xlabel('Number of clusters (k)')
    axs[2].set_ylabel('Davies-Bouldin Index')
    axs[2].set_title('Davies-Bouldin Index Method')

    plt.show()


def metric_cluster(scaled):
    inertia = []
    silhouette = []
    db_scores = []
    for k in range(2, 11):
        kmeans = KMeans(n_clusters=k, random_state=42)
        kmeans.fit(scaled)
        inertia.append(kmeans.inertia_)
        silhouette.append(silhouette_score(scaled, kmeans.predict(scaled)))
        db_scores.append(davies_bouldin_score(scaled, kmeans.labels_))

    results_df = pd.DataFrame({'Number_Cluster': range(2, 11),
                           'Inertia': inertia,
                           'Silhouette': silhouette,
                           'DBI': db_scores})
    return results_df  

def get_cluster_stats_median(df_cluster, features):
    #cluster features by median
    cluster_stats = pd.DataFrame(columns=features)
    
    for n in df_cluster['Cluster_features'].value_counts().index.to_list():   
        cluster_stats = cluster_stats.append(df_cluster[df_cluster['Cluster_features'] == n][features].median(), ignore_index=True)
    
    return cluster_stats



def radar_plot(cluster_stats):
    # radar plot with 4 variables
    mpl.rcParams['figure.figsize'] = (10, 10)
    categories = list(cluster_stats)
    # Calculate the angles for each category
    N = len(categories)
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]
    # Create the plot
    ax = plt.subplot(111, polar=True)
    # Set the starting angle at the top and rotate in a clockwise direction
    ax.set_theta_offset(pi / 2)
    ax.set_theta_direction(-1)
    # Set the labels for each category
    plt.xticks(angles[:-1], categories)
    # Set the position of the radial axis labels
    ax.set_rlabel_position(-22.5)
    # Set the y-axis tick labels and limits
    plt.yticks([-2, -1.5,-1, -0.5, 0, 0.5, 1, 1.5, 2], ["-2","-1.5",'-1', '-0.5', '0', '0.5', '1', "1.5", "2"], color='grey', size=7)
    plt.ylim(-2,2)
    # Define colors for each cluster
    colors = ['purple', 'green','yellow', "blue"]
    # Plot each cluster
    for i in range(len(cluster_stats)):
        values = cluster_stats.iloc[i].values.flatten().tolist()
        values += values[:1]
        ax.plot(angles, values, linewidth=1, linestyle='solid', label=f'Cluster {i}', color=colors[i])
        ax.fill(angles, values, alpha=0.1)
    # Add the legend
    plt.legend(loc='upper right', bbox_to_anchor=(0.1,0.1))
    return plt.gcf()

def heatmap_correlation_features(df, features_columns):
    corr_matrix = df[features_columns].corr()
    mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
    sns.heatmap(corr_matrix, mask=mask, cmap="Greens", annot=True, fmt=".2f")
    plt.title("Correlations between features")
    plt.tight_layout()
    return plt.gcf()
    
def boxplot_features_cluster(df,Cluster_features_column, features_columns):
    colors = ['purple', 'green','yellow', "blue"]
    # Create boxplot for every feature
    fig, axs = plt.subplots(2, 3, figsize=(16, 8))
    axs = axs.flatten() 
    for i, feature in enumerate(features_columns):
        sns.boxplot(x=df[Cluster_features_column], y=df[feature], palette=colors, ax=axs[i])
        axs[i].set_title(f'Boxplot {feature} by Cluster')
        axs[i].set_xlabel('Cluster')
        axs[i].set_ylabel(feature)

    plt.tight_layout()#amazing 
    plt.show()
