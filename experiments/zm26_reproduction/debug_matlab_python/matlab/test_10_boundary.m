function test_10_boundary()
%TEST_10_BOUNDARY  pre/post bound repair of GA.m using shared streams.
    P = setup_diag();
    G = ensure_global_mpdmp4(20, 100000);
    parents = diag_load_csv(fullfile(P.shared, 'variation_parents.csv'));
    mu_sbx = diag_load_csv(fullfile(P.shared, 'ga_mu_sbx.csv'));
    sign01 = diag_load_csv(fullfile(P.shared, 'ga_sign_sbx.csv'));
    beta_skip = diag_load_csv(fullfile(P.shared, 'ga_beta_skip.csv'));
    proc = diag_load_csv(fullfile(P.shared, 'ga_proc.csv'));
    site_u = diag_load_csv(fullfile(P.shared, 'ga_site.csv'));
    mu_mut = diag_load_csv(fullfile(P.shared, 'ga_mu_mut.csv'));
    [post, pre] = ga_from_stream(parents, G.lower, G.upper, mu_sbx, sign01, ...
        beta_skip, proc, site_u, mu_mut, 1, 15, 0.5, 20);
    was_out = any(pre < 0 | pre > 100, 2);
    data = [(1:size(post,1))', pre, post, double(was_out)];
    diag_write_csv(fullfile(P.out, 'test_10_boundary.csv'), ...
        {'off_id','pre_x1','pre_x2','post_x1','post_x2','was_outside'}, data);
    fid = fopen(fullfile(P.out, 'test_10_notes.txt'), 'w');
    fprintf(fid, 'GA.m clips with min(max(x,lower),upper) after SBX and before PM.\n');
    fprintf(fid, 'GA.m does not clip after PM; INDIVIDUAL constructor then clips.\n');
    fprintf(fid, 'Diagnostic ga_from_stream also clips after PM to match INDIVIDUAL.\n');
    fprintf(fid, 'No reflect / regenerate / midpoint repair.\n');
    fclose(fid);
    fprintf('matlab test_10 done  n_outside_pre=%d\n', sum(was_out));
end
