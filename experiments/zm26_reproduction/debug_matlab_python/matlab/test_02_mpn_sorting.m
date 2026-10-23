function test_02_mpn_sorting()
%TEST_02_MPN_SORTING  NDSort per DM + MPNDS + PLNDS on shared F.
    P = setup_diag();
    G = ensure_global_mpdmp4(20, 100000);
    F = diag_load_csv(fullfile(P.shared, 'mpnds_F.csv'));
    n = size(F, 1);
    DM = G.DM;
    front_DM1 = NDSort(F(:, DM{1}), n);
    front_DM2 = NDSort(F(:, DM{2}), n);
    [combined, max_fno] = MPNDS(F, n, DM);
    [pl, max_pl] = PLNDS(F, n, DM);
    data = [(1:n)', front_DM1(:), front_DM2(:), combined(:), pl(:)];
    diag_write_csv(fullfile(P.out, 'test_02_mpn_sorting.csv'), ...
        {'point_id','front_DM1','front_DM2','combined_front','plnds_front'}, data);
    diag_write_csv(fullfile(P.out, 'test_02_meta.csv'), {'field_id','value'}, [1, max_fno; 2, max_pl]);
    fprintf('matlab test_02 done  max_fno_mpnds=%g\n', max_fno);
end
