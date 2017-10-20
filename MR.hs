head' :: [a] -> a 
head' (x:xs) = x

tail' :: [a] -> [a]
tail' [] = []
tail' (x:xs) = xs

take' :: Int -> [a] -> [a]
take' 0 _ = []
take' _ [] = []
take' n (x:xs) = [x] ++ (take' (n - 1) xs)

drop' :: Int -> [a] -> [a]
drop' 0 x = x
drop' _ [] = []
drop' n (x:xs) = drop' (n - 1) xs

filter' :: (a -> Bool) -> [a] -> [a]
filter' _ [] = []
filter' f (x:xs) = if (f x) then [x] ++ (filter' f xs) else filter' f xs

foldl' :: (a -> b -> a) -> a -> [b] -> a
foldl' _ z [] = z
foldl' f z (x:xs) = foldl' f (f z x) xs

concat' :: [a] -> [a] -> [a]
concat' [] y = y
concat' (x:xs) y = x:(concat' xs y) 

quickSort' :: Ord a => [a] -> [a]
quickSort [] = []
quickSort' (x:xs) = concat' (concat' (filter' (<=x) xs) [x]) (filter' (>x) xs)

--main = print (quickSort' [1,6,0])


