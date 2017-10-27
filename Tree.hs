import Prelude hiding (lookup)

-- Implement a binary search tree (4 points)
-- 2 extra points for a balanced tree


data BinaryTree k v = Null | Node k v (BinaryTree k v) (BinaryTree k v) deriving Show

-- “Ord k =>” requires, that the elements of type k are comparable
-- Takes a key and a tree and returns Just value if the given key is present,
-- otherwise returns Nothing

lookup :: Ord k => k -> BinaryTree k v -> Maybe v
lookup fnd Null = Nothing
lookup fnd (Node k v l r) | (k > fnd)  = lookup fnd l 
                          | (k < fnd)  = lookup fnd r
                          | (fnd == k) = Just v

-- Takes a key, value and tree and returns a new tree with key/value pair inserted.
-- If the given key was already present, the value is updated in the new tree.
insert :: Ord k => k -> v -> BinaryTree k v -> BinaryTree k v
insert k v Null = (Node k v Null Null)
insert newK newV (Node k v l r) | (newK < k) = (Node k v (insert newK newV l) r)
                                | (newK > k) = (Node k v l (insert newK newV r)) 
                                | (newK == k) = (Node newK newV l r) 

minK :: BinaryTree k v -> k
minK (Node k v Null r) = k
minK (Node k v l r) = minK l

minV :: BinaryTree k v -> v
minV (Node k v Null r) = v
minV (Node k v l r) = minV l

delMin :: BinaryTree k v -> BinaryTree k v
delMin (Node k v Null r) = r
delMin (Node k v l r) = (Node k v (delMin l) r)

extractRoot :: BinaryTree k v -> BinaryTree k v
extractRoot (Node k v l Null) = l
extractRoot (Node k v l r) = (Node (minK r) (minV r) l (delMin r))

-- Returns a new tree without the given key
delete :: Ord k => k -> BinaryTree k v -> BinaryTree k v
delete delK Null = Null
delete delK (Node k v l r) | (delK < k)  = (Node k v (delete delK l) r)
                           | (delK > k)  = (Node k v l (delete delK r))
                           | (delK == k) = (extractRoot (Node k v l r))


--tree1 = Null
--tree2 = insert 3 3 tree1
--tree = delete 3 tree2
--tree3 = insert 2 2 tree2
--tree4 = insert 1 1 tree3
--tree5 = insert 4 4 tree4
--tree6 = insert 5 5 tree5

--main = print( lookup 3 tree2 )
--main = print( lookup 3 tree )
--main = print( lookup 4 tree6 )