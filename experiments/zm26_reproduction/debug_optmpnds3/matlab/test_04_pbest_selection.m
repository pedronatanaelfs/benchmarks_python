function test_04_pbest_selection()
    P = setup_diag();
    front = diag_load_csv(fullfile(P.shared, 'pbest_front.csv'));
    crowd = diag_load_csv(fullfile(P.shared, 'pbest_crowd.csv'));
    ks = diag_load_csv(fullfile(P.shared, 'pbest_k.csv'));
    n = numel(ks);
    out = zeros(n, 4);
    for i = 1:n
        idx = getBestIndividualFromK(front(:)', crowd(:)', ks(i));
        out(i,:) = [i, ks(i), idx, front(idx)];
    end
    diag_write_csv(fullfile(P.out, 'test_04_pbest_selection.csv'), ...
        {'point_id','k','matlab_index_1based','matlab_front'}, out);
    fprintf('matlab test_04 done n=%d\n', n);
end
