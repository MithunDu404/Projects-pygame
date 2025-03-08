#include<iostream> 
#include<vector>
#include<algorithm>
using namespace std;

class DSU{
    int* parent;
    int* rank;
    public:
    DSU(int n){
        parent = new int[n];
        rank = new int[n];
        for(int i=0;i<n;i++){
            parent[i] = i;
            rank[i] = 1;
        }
    }
    int Find(int x){
        if(x == parent[x]) return x;
        else return parent[x] = Find(parent[x]);
    }
    void Union(int x,int y){
        int x_parent = Find(x);
        int y_parent = Find(y);
        if(x_parent == y_parent) return;
        if(rank[x_parent] > rank[y_parent]){
            parent[y_parent] = x_parent;
        }
        else if(parent[x_parent] < parent[y_parent]){
            parent[x_parent] = y_parent;
        }
        else{
            parent[x_parent] = y_parent;
            rank[y_parent]++;
        }
    }
};

void MST_kruskal(int V,vector<vector<vector<int>>>& adjList){
    vector<vector<int>> edges;
    for(int u=0;u<V;u++){
        for(auto edge : adjList[u]){
            int v = edge[0];
            int w = edge[1];
            edges.push_back({w,u,v});
        }
    }
    sort(edges.begin(),edges.end());
    DSU dsu(V);
    int cost = 0;
    for(auto edge : edges){
        int w = edge[0];
        int u = edge[1];
        int v = edge[2];
        if(dsu.Find(u) != dsu.Find(v)){
            cout<<u<<" "<<v<<" "<<w<<endl;
            dsu.Union(u,v);
            cost += w;
        }
    }
}

int main(){
    int V,E;
    cin>>V>>E;
    vector<vector<vector<int>>> adjList(V);
    for(int i=0;i<E;i++){
        int u,v,w;
        cin>>u>>v>>w;
        adjList[u].push_back({v,w});
        adjList[v].push_back({u,w});
    }
    MST_kruskal(V,adjList);
    return 0;
}