# Common Algorithms

For leetcode problems, the Python3 Solutions are published in jupyter notebook (*still in progress*). Check out more in [Jupyter nbviewer](https://nbviewer.jupyter.org/github/darrenfu/LeetcodePy/tree/master/jupyter-notebook/).

Here, I summarized top common algorithms to deal with classic leetcode problems.

### Binary Search
1. Search for exact match
    * [349. Intersection of Two Arrays](https://nbviewer.jupyter.org/github/darrenfu/LeetcodePy/tree/master/jupyter-notebook/0349.intersection-of-two-arrays.ipynb)
    * [350. Intersection of Two Arrays II](https://nbviewer.jupyter.org/github/darrenfu/LeetcodePy/tree/master/jupyter-notebook/0350.intersection-of-two-arrays-ii.ipynb)
1. Search for position to insert
    * [Patience Sorting](http://wordaligned.org/articles/patience-sort)
    * [300. Longest Increasing Subsequence](https://nbviewer.jupyter.org/github/darrenfu/LeetcodePy/tree/master/jupyter-notebook/0300.longest-increasing-subsequence.ipynb)
    * [354. Russian Doll Envelopes](https://nbviewer.jupyter.org/github/darrenfu/LeetcodePy/tree/master/jupyter-notebook/0354.russian-doll-envelopes.ipynb)
    * [363. Max Sum of Rectangle No Larger Than K](https://nbviewer.jupyter.org/github/darrenfu/LeetcodePy/tree/master/jupyter-notebook/0363.max-sum-of-rectangle-no-larger-than-k.ipynb)
    * [367. Valid Perfect Square](https://nbviewer.jupyter.org/github/darrenfu/LeetcodePy/tree/master/jupyter-notebook/0367.valid-perfect-square.ipynb)
    * [441. Arranging Coins](https://nbviewer.jupyter.org/github/darrenfu/LeetcodePy/tree/master/jupyter-notebook/0441.arranging-coins.ipynb)
    * [475. Heaters](https://nbviewer.jupyter.org/github/darrenfu/LeetcodePy/tree/master/jupyter-notebook/0475.heaters.ipynb)
    * [611. Valid Triangle Number](https://nbviewer.jupyter.org/github/darrenfu/LeetcodePy/tree/master/jupyter-notebook/0611.valid-triangle-number.ipynb)
1. Sub-function (hard)
    * [410. Split Array Largest Sum](https://nbviewer.jupyter.org/github/darrenfu/LeetcodePy/tree/master/jupyter-notebook/0410.split-array-largest-sum.ipynb)
    * [774. Minimize Max Distance to Gas Station](https://nbviewer.jupyter.org/github/darrenfu/LeetcodePy/tree/master/jupyter-notebook/0774.minimize-max-distance-to-gas-station.ipynb)
    * [875. Koko Eating Bananas](https://nbviewer.jupyter.org/github/darrenfu/LeetcodePy/tree/master/jupyter-notebook/0875.koko-eating-bananas.ipynb)
    * [1011. Capacity To Ship Packages In N Days](https://nbviewer.jupyter.org/github/darrenfu/LeetcodePy/tree/master/jupyter-notebook/1011.capacity-to-ship-packages-within-d-days.ipynb)
    * [1231. Divide Chocolate](https://nbviewer.jupyter.org/github/darrenfu/LeetcodePy/tree/master/jupyter-notebook/1231.divide-chocolate.ipynb)
    * [1283. Find the Smallest Divisor Given a Threshold](https://nbviewer.jupyter.org/github/darrenfu/LeetcodePy/tree/master/jupyter-notebook/1283.find-the-smallest-divisor-given-a-threshold.ipynb)
    
### Tree  
1. Post-order Traversal Tree Problems
    * [124. Binary Tree Maximum Path Sum](https://nbviewer.jupyter.org/github/darrenfu/LeetcodePy/tree/master/jupyter-notebook/0124.binary-tree-maximum-path-sum.ipynb)
    * [250. Count Univalue Subtrees](https://nbviewer.jupyter.org/github/darrenfu/LeetcodePy/tree/master/jupyter-notebook/0250.count-univalue-subtrees.ipynb)
    * [298. Binary Tree Longest Consecutive Sequence](https://nbviewer.jupyter.org/github/darrenfu/LeetcodePy/tree/master/jupyter-notebook/0298.binary-tree-longest-consecutive-sequence.ipynb)
    * [508. Most Frequent Subtree Sum](https://nbviewer.jupyter.org/github/darrenfu/LeetcodePy/tree/master/jupyter-notebook/0508.most-frequent-subtree-sum.ipynb)
    * [543. Diameter of Binary Tree](https://nbviewer.jupyter.org/github/darrenfu/LeetcodePy/tree/master/jupyter-notebook/0543.diameter-of-binary-tree.ipynb)
    * [549. Binary Tree Longest Consecutive Sequence II](https://nbviewer.jupyter.org/github/darrenfu/LeetcodePy/tree/master/jupyter-notebook/0549.binary-tree-longest-consecutive-sequence-ii.ipynb)
    * [687. Longest Univalue Path](https://nbviewer.jupyter.org/github/darrenfu/LeetcodePy/tree/master/jupyter-notebook/0687.longest-univalue-path.ipynb)
    * [1245. Tree Diameter](https://nbviewer.jupyter.org/github/darrenfu/LeetcodePy/tree/master/jupyter-notebook/1245.tree-diameter.ipynb)
    * [Max Path Sum in a Grid](https://leetcode.com/discuss/interview-question/391278/google-phone-screen-maximal-path-sum/351744)
    * [Maximum number of unique prime factors](https://www.geeksforgeeks.org/maximum-number-unique-prime-factors/)
1. Segment Tree / Binary Indexed Tree (Fenwick Tree)
1. Morris Tree Traversal

### Graph  
1. Disjoint Sets (Union Find)
    * [200. Number of Islands]()
    * [947. Most Stones Removed with Same Row or Column]()
1. Shortest Paths Problems
    * Dijkstra
        * [787. Cheapest Flights Within K Stops]()
        * [1162. As Far from Land as Possible]()
    * Floyd-Warshall
    * Bellman-Ford
    * SPFA
        * [1162. As Far from Land as Possible]()
    * BFS
        * [365. Water and Jug Problem]()
        * [994. Rotting Oranges]()
        * [1162. As Far from Land as Possible]()
    * Bidirectional
        * [127. Word Ladder]()
        * [126. Word Ladder II]()
        * [433. Minimum Genetic Mutation]()
    * Multisource BFS
        * [317. Shortest Distance from All Buildings]()
        * [1162. As Far from Land as Possible]()
1. Kahn's Algorithm - Topological sorting  
    * [207. Course Scheduling](https://nbviewer.jupyter.org/github/darrenfu/LeetcodePy/tree/master/jupyter-notebook/0207.course-schedule.ipynb)
    * [310. Minimum Height Trees]()
    * [1203. Sort items by groups respecting dependencies](https://nbviewer.jupyter.org/github/darrenfu/LeetcodePy/tree/master/jupyter-notebook/1203.sort-items-by-groups-respecting-dependencies.ipynb)
1. Cycle Detection Algorithms
    * Tricolor DFS
        * [785. Is Graph Bipartite?]()
        * [802. Find Eventual Safe States]()
        * [1059. All Paths from Source Lead to Destination]()
    * Floyd's Tortoise and Hare
1. DFS
    * [365. Water and Jug Problem]()
1. Tarjan's algorithm  
   Strongly Connected Components (SCC)  
   * [928. Minimize Malware Spread II]()
   * [1192. Critical Connections in a Network]()
1. Kruskal's Algorithm
1. Maze router Problems
    * Lee algorithm
1. Euler Path (Hierholzer's algorithm)
    * [332. Reconstruct Itinerary](https://nbviewer.jupyter.org/github/darrenfu/LeetcodePy/tree/master/jupyter-notebook/0332.reconstruct-itinerary.ipynb)
   
### Dynamic Programming  
1. Permutations and Combinations
    * [31. Permutation](https://nbviewer.jupyter.org/github/darrenfu/LeetcodePy/tree/master/jupyter-notebook/0031.next-permutation.ipynb)
    * [46. Permutations](https://nbviewer.jupyter.org/github/darrenfu/LeetcodePy/tree/master/jupyter-notebook/0046.permutations.ipynb)
    * [47. Permutations II](https://nbviewer.jupyter.org/github/darrenfu/LeetcodePy/tree/master/jupyter-notebook/0047.permutations-ii.ipynb)
    * [60. Permutation Sequence](https://nbviewer.jupyter.org/github/darrenfu/LeetcodePy/tree/master/jupyter-notebook/0060.permutation-sequence.ipynb)
    * [78. Subsets](https://nbviewer.jupyter.org/github/darrenfu/LeetcodePy/tree/master/jupyter-notebook/0078.subsets.ipynb)
    * [90. Subsets II](https://nbviewer.jupyter.org/github/darrenfu/LeetcodePy/tree/master/jupyter-notebook/0090.subsets-ii.ipynb)
    * [1255. Maximum Score Words Formed by Letters](https://nbviewer.jupyter.org/github/darrenfu/LeetcodePy/tree/master/jupyter-notebook/1255.maximum-score-words-formed-by-letters.ipynb)
    * [1286. Iterator for Combination](https://nbviewer.jupyter.org/github/darrenfu/LeetcodePy/tree/master/jupyter-notebook/1286.iterator-for-combination.ipynb)
1. Knapsack problem
    1. 0/1 Knapsack 
        * [416. Partition Equal Subset Sum](https://nbviewer.jupyter.org/github/darrenfu/LeetcodePy/tree/master/jupyter-notebook/0416.partition-equal-subset-sum.ipynb)
        * [871. Minimum Number of Refueling Stops](https://nbviewer.jupyter.org/github/darrenfu/LeetcodePy/tree/master/jupyter-notebook/0871.minimum-number-of-refueling-stops.ipynb)
    1. Complete Knapsack 
        * [279. Perfect Squares](https://nbviewer.jupyter.org/github/darrenfu/LeetcodePy/tree/master/jupyter-notebook/0279.perfect-squares.ipynb)
        * [322. Coin Change](https://nbviewer.jupyter.org/github/darrenfu/LeetcodePy/tree/master/jupyter-notebook/0322.coin-change.ipynb)
        * [377. Combination Sum IV]()
        * [518. Coin Change 2](https://nbviewer.jupyter.org/github/darrenfu/LeetcodePy/tree/master/jupyter-notebook/0518.coin-change-2.ipynb)
1. Kadane's algorithm (DP approach to solve the largest contiguous elements in an array)
    * [53. Maximum Subarray](https://nbviewer.jupyter.org/github/darrenfu/LeetcodePy/tree/master/jupyter-notebook/0053.maximum-subarray.ipynb)
    * [978. Longest Turbulent Subarray](https://nbviewer.jupyter.org/github/darrenfu/LeetcodePy/tree/master/jupyter-notebook/0978.longest-turbulent-subarray.ipynb)
    * [1186. Maximum Subarray Sum with One Deletion](https://nbviewer.jupyter.org/github/darrenfu/LeetcodePy/tree/master/jupyter-notebook/1186.maximum-subarray-sum-with-one-deletion.ipynb)
    * [1191. K-Concatenation Maximum Sum](https://nbviewer.jupyter.org/github/darrenfu/LeetcodePy/tree/master/jupyter-notebook/1191.k-concatenation-maximum-sum.ipynb)
1. Two-dimensional DP
    * LIS series
        * [300. Longest Increasing Subsequence]()
        * [491. Increasing Subsequences]()
    * LCS series
        * [1143. Longest Common Subsequence]()
        * [1092. Shortest Common Supersequence]() - SCS
        * [516. Longest Palindromic Subsequence]()
        * [1216. Valid Palindrome III]()
        * [72. Edit Distance]()
        * [673. Number of Longest Increasing Subsequence]()
    * Palindromic Substring
        **Other Solution**: Middle-to-two-ends / Manacher  
        * [5. Longest Palindromic Substring]()
        * [214. Shortest Palindrome]()
        * [647. Palindromic Substrings]()
1. [Game Theory](https://leetcode.com/tag/minimax/)
    **Other Solution**: MinMax
    * [292. Nim Game]()
    * [464. Can I Win]()
    * [486. Predict the Winner]()
    * [1025. Divisor Game]()
    * [877. Stone Game]()
    * [1140. Stone Game II]()
    * [5 Pirates and 100 Gold Coins](https://www.geeksforgeeks.org/puzzle-20-5-pirates-and-100-gold-coins/)
    * [LintCode 394. Coins in a Line](https://www.lintcode.com/problem/coins-in-a-line/description)
    * [LintCode 395. Coins in a Line II](https://www.lintcode.com/problem/coins-in-a-line-ii/description)

### Misc  
1. Interval Scheduling  
   **Solution**: Greedy / Boundary Counting
    * [56. Merge Intervals]()
    * [252. Meeting Rooms]()
    * [253. Meeting Rooms II]()
    * [435. Non-overlapping Intervals]()
    * [452. Minimum Number of Arrows to Burst Balloons]()
    * [57. Insert Interval]()
    * [352. Data Stream as Disjoint Intervals]()
    * [436. Find Right Interval]()
    * [616. Add Bold Tag in String]()
    * [636. Exclusive Time of Functions]()
    * [646. Maximum Length of Pair Chain]()
    * [699. Falling Squares]()
    * [715. Range Module]()
    * [729. My Calendar I]()
    * [731. My Calendar II]()
    * [732. My Calendar III]()
    * [759. Employee Free Time]()
    * [986. Interval List Intersections]()
    * [1109. Corporate Flight Bookings]()
    * [1235. Maximum Profit in Job Scheduling]()
    * [1288. Remove Covered Intervals]() - Boundary Counting doesn't work?
1. Sliding window
    * Easy
        * [643. Maximum Average Subarray I]()
    * Hard
        * [727. Minimum Window Subsequence](https://nbviewer.jupyter.org/github/darrenfu/LeetcodePy/tree/master/jupyter-notebook/0727.minimum-window-subsequence.ipynb)
        * [904. Fruit Into Baskets](https://nbviewer.jupyter.org/github/darrenfu/LeetcodePy/tree/master/jupyter-notebook/0904.fruit-into-baskets.ipynb)
        * [992. Subarrays with K Different Integers](https://nbviewer.jupyter.org/github/darrenfu/LeetcodePy/tree/master/jupyter-notebook/0992.subarrays-with-k-different-integers.ipynb)
        * [1234. Replace the Substring for Balanced String](https://nbviewer.jupyter.org/github/darrenfu/LeetcodePy/tree/master/jupyter-notebook/1234.replace-the-substring-for-balanced-string.ipynb)
    * Substring search [Template](https://leetcode.com/problems/find-all-anagrams-in-a-string/discuss/92007/Sliding-Window-algorithm-template-to-solve-all-the-Leetcode-substring-search-problem)
        * [3. Longest Substring Without Repeating Characters]()
        * [30. Substring with Concatenation of All Words]()
        * [76. Minimum Window Substring]()
        * [159. Longest Substring with At Most Two Distinct Characters]()
        * [340. Longest Substring with At Most K Distinct Characters]()
        * [438. Find All Anagrams in a String]()
1. PreSum
    * Easy
        * [53. Maximum Subarray]()
        * [643. Maximum Average Subarray I]()
1. Stack
    1. Monotonic stack
        * [42. Trapping Rain Water]()
        * [84. Largest Rectangle in Histogram]()
        * [581. Shortest Unsorted Continuous Subarray]()
        * [739. Daily Temperatures]()
    1. RPN (Reversed Polish Notation)
        * [224. Basic Calculator]()
        * [227. Basic Calculator II]()
        * [772. Basic Calculator III]()
        * [770. Basic Calculator IV]() - Hard
    1. Good stack problems
        * [388. Longest Absolute File Path]()
        * [496. Next Greater Element I]()
        * [503. Next Greater Element II]()
        * [636. Exclusive Time of Functions]()
        * [856. Score of Parentheses]()
        * [901. Online Stock Span]()
        * [907. Sum of Subarray Minimums]()
        * [1111. Maximum Nesting Depth of Two Valid Parentheses Strings]()
        * [1130. Minimum Cost Tree From Leaf Values]()
1. Bit Operation
    * [137. Single Number II]()
    * [318. Maximum Product of Word Lengths]()
1. Sieve of Eratosthenes
    * [204. Count Primes](https://nbviewer.jupyter.org/github/darrenfu/LeetcodePy/tree/master/jupyter-notebook/0204.count-primes.ipynb)
    * [Number which has the maximum number of distinct prime factors in the range M to N](https://www.geeksforgeeks.org/number-which-has-the-maximum-number-of-distinct-prime-factors-in-range-m-to-n/)
1. Integer Factorization
1. Fourier Transform
1. Modulo Arithmetic
1. Link Analysis  
1. Reservoir Sampling  
1. Boyer-Moore Majority Vote algorithm  
1. Bézout's identity (GCD)
    * [365. Water and Jug Problem]()
    * [1250. Check If It Is a Good Array]()
1. Euclidean
    * [780. Reaching Points]()
1. SLR(1) 
    * [282. Expression Add Operators](https://nbviewer.jupyter.org/github/darrenfu/LeetcodePy/tree/master/jupyter-notebook/0282.expression-add-operators.ipynb)
1. DFA - Deterministic Finite Automaton  
    * [10. Regular Expression Matching](https://nbviewer.jupyter.org/github/darrenfu/LeetcodePy/tree/master/jupyter-notebook/0010.regular-expression-matching.ipynb)
    * [65. Valid Number](https://nbviewer.jupyter.org/github/darrenfu/LeetcodePy/tree/master/jupyter-notebook/0065.valid-number.ipynb)
1. Round Robin
    * [68. Text Justification](https://nbviewer.jupyter.org/github/darrenfu/LeetcodePy/tree/master/jupyter-notebook/0068.text-justification.ipynb)
Use case: Find the majority element in a list of values. Check this [article](https://gregable.com/2013/10/majority-vote-algorithm-find-majority.html).  
    * [169. Majority Element](https://nbviewer.jupyter.org/github/darrenfu/LeetcodePy/tree/master/jupyter-notebook/0169.majority-element.ipynb)
    * [229. Majority Element II](https://nbviewer.jupyter.org/github/darrenfu/LeetcodePy/tree/master/jupyter-notebook/0229.majority-element-ii.ipynb)
    * [1150. Check If a Number Is Majority Element in a Sorted Array](https://nbviewer.jupyter.org/github/darrenfu/LeetcodePy/tree/master/jupyter-notebook/1150.check-if-a-number-is-majority-element-in-a-sorted-array.ipynb)
    * [1157. Online Majority Element In Subarray](https://nbviewer.jupyter.org/github/darrenfu/LeetcodePy/tree/master/jupyter-notebook/1157.online-majority-element-in-subarray.ipynb)

### Tricky Solutions  
    * [65. Valid Number]() - DFA
    * [136. Single Number]() - XOR
    * [240. Search a 2D Matrix II]() - Start from Right-top Corner

### String
1. TBD

