class BinaryIndexTree(object):
    def __init__(self, values):
        self.values = values
        n = len(self.values)
        self.tree = [0] * (n + 1)

        # populate the tree
        for i, value in enumerate(values):
            i += 1
            while i <= n:
                self.tree[i] += value
                # get the first nonzero bit (from lowest)
                i += i & (-i)

    # Returns sum of arr[0..index]. This function assumes
    # that the array is preprocessed and partial sums of
    # array elements are stored in BITree[].
    def getSum(self, i):
        s = 0  # initialize result

        # index in BITree[] is 1 more than the index in arr[]
        i = i + 1

        # Traverse ancestors of tree[index]
        while i > 0:
            # Add current element of BITree to sum
            s += self.tree[i]

            # Move index to parent node in getSum View
            i -= i & (-i)
        return s

    def update(self, i, value):
        mod = value - self.values[i]
        self.values[i] = value

        i += 1
        while i <= len(self.values):
            self.tree[i] += mod
            i += i & (-i)
