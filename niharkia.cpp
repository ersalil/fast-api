#include<bits/stdc++.h>
using namespace std;

int main()
{
    // input 2 nos.
    int a,b;
    cin>>a>>b;
    // print the sum of the nos.
    int c = a/b;
    int ans1, ans2;
    ans1 = c*b;
    ans2 = (c+1)*b;
    // return ans1 or ans2 closer to a
    if(abs(a-ans1)<abs(a-ans2))
    {
        cout<<ans1;
    }
    else
    {
        cout<<ans2;
    }
    return 0;
}