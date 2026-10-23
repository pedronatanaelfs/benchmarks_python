function test_08_unique_rows()
%TEST_08_UNIQUE_ROWS  MATLAB unique(...,'rows') on a duplicate population.
    P = setup_diag();
    G = ensure_global_mpdmp4(7, 100000);
    X = diag_load_csv(fullfile(P.shared, 'unique_X.csv'));
    F = G.problem.CalObj(X);
    [Fu, ia, ic] = unique(F, 'rows');
    [~, ia_first, ~] = unique(F, 'rows', 'first');
    [~, ia_last, ~] = unique(F, 'rows', 'last');
    n = size(X, 1);
    map = [(1:n)', ic(:), ia(ic), ia_first(ic), ia_last(ic)];
    diag_write_csv(fullfile(P.out, 'test_08_unique_map.csv'), ...
        {'input_index','duplicate_group','retained_index_default','retained_index_first','retained_index_last'}, map);
    kept = [ia(:), ia_first(:), ia_last(:), (1:numel(ia))'];
    diag_write_csv(fullfile(P.out, 'test_08_unique_kept.csv'), ...
        {'kept_input_index','kept_first','kept_last','unique_order'}, kept);
    % Also export unique on decision rows
    [Xu, iaX, icX] = unique(X, 'rows');
    diag_write_csv(fullfile(P.out, 'test_08_unique_X_kept.csv'), ...
        {'kept_input_index','unique_order'}, [iaX(:), (1:numel(iaX))']);
    fprintf('matlab test_08 done  n_unique_F=%d  n_unique_X=%d\n', size(Fu,1), size(Xu,1));
end
