#include <bits/stdc++.h>
using namespace std;

#define int long long
#define fast_io                       \
    ios_base::sync_with_stdio(false); \
    cin.tie(nullptr);
const int N = 1e5 + 10;
// vector<int> dp(N, -1);
int a[N], tree[4 * N];

// vector<vector<int>> dp( N , vector<int> (M, 0));

void build(int node, int st, int en) // node-->starting node
{
    if (st == en)
    {
        tree[node] = a[st];
        return;
    }

    int mid = (st + en) / 2;

    build(2 * node, st, mid);
    build(2 * node + 1, mid + 1, en);

    // important line
    tree[node] = max(tree[2 * node], tree[2 * node + 1]);
}

int query(int node, int st, int en, int l, int r)
{
    if (st > r || en < l)
        return INT_MIN;
    if (st >= l && en <= r)
        return tree[node];

    int mid = (st + en) / 2;

    int q1 = query(2 * node, st, mid, l, r);
    int q2 = query(2 * node + 1, mid + 1, en, l, r);

    return max(q1, q2);
}

void update(int node, int st, int en, int idx, int val)
{
    if (st == en)
    {
        a[st] = val;
        tree[node] = val;
        return;
    }

    int mid = (st + en) / 2;

    if (idx <= mid)
    {
        update(2 * node, st, mid, idx, val);
    }
    else
        update(2 * node + 1, mid + 1, en, idx, val);

    tree[node] = max(tree[2 * node + 1], tree[2 * node]);
}

signed main()
{
    fast_io
    int test;
    cin>>test;
    while(test--)
    {
    
    int n;
    cin >> n;
    for (int i = 0; i < n; i++)
    {
        cin >> a[i];
    }

    build(1, 0, n - 1);

    for(int i=1;i<=4*n;i++)
    {
        cout<<tree[i]<<" ";
    }

    }

    return 0;
}