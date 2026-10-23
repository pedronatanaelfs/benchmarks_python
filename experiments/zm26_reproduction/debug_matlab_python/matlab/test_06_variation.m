function test_06_variation()
%TEST_06_VARIATION  SBX+PM from shared random streams (MATLAB GA.m rate proM/D).
    P = setup_diag();
    G = ensure_global_mpdmp4(20, 100000);
    parents = diag_load_csv(fullfile(P.shared, 'variation_parents.csv'));
    mu_sbx = diag_load_csv(fullfile(P.shared, 'ga_mu_sbx.csv'));
    sign01 = diag_load_csv(fullfile(P.shared, 'ga_sign_sbx.csv'));
    beta_skip = diag_load_csv(fullfile(P.shared, 'ga_beta_skip.csv'));
    proc = diag_load_csv(fullfile(P.shared, 'ga_proc.csv'));
    site_u = diag_load_csv(fullfile(P.shared, 'ga_site.csv'));
    mu_mut = diag_load_csv(fullfile(P.shared, 'ga_mu_mut.csv'));
    [off, pre] = ga_from_stream(parents, G.lower, G.upper, mu_sbx, sign01, ...
        beta_skip, proc, site_u, mu_mut, 1, 15, 0.5, 20);
    n_out = sum(any(pre < 0 | pre > 100, 2));
    diag_write_csv(fullfile(P.out, 'test_06_offspring_matlab_rate.csv'), {'x1','x2'}, off);
    diag_write_csv(fullfile(P.out, 'test_06_pre_repair_matlab_rate.csv'), {'x1','x2'}, pre);
    diag_write_csv(fullfile(P.out, 'test_06_meta.csv'), {'field_id','value'}, ...
        [(1:5)', [1; 15; 0.5; 20; n_out]]);
    fprintf('matlab test_06 done  n_pre_repair_outside=%d\n', n_out);
end
