function idx = getBestIndividualFromK(FrontNo, CrowdDis, k)
%GETBESTINDIVIDUALFROMK  getBestIndividual.m with k supplied (1-based).
    index = 0;
    count = 0;
    while count < k
        index = index + 1;
        tmp = length(find(FrontNo == index));
        count = count + tmp;
        if index > 10000
            error('front walk failed');
        end
    end
    count = length(find(FrontNo < index));
    Last = find(FrontNo == index);
    [~, Rank] = sort(CrowdDis(Last), 'descend');
    Next = Last(Rank(k - count));
    idx = Next;
end
