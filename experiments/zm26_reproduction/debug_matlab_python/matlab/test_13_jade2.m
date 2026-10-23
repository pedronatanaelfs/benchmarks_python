function test_13_jade2()
%TEST_13_JADE2  Documented one-step current-to-pbest using shared indices.
% OptMPNDS3 only. Not required to pass before OptMPNDS is diagnosed.
    P = setup_diag();
    G = ensure_global_mpdmp4(8, 100000);
    X = diag_load_csv(fullfile(P.shared, 'jade_X.csv'));
    cr = diag_load_csv(fullfile(P.shared, 'jade_cr.csv'));
    Fs = diag_load_csv(fullfile(P.shared, 'jade_F.csv'));
    pbest_idx = diag_load_csv(fullfile(P.shared, 'jade_pbest_idx.csv')); % 0-based
    i1 = diag_load_csv(fullfile(P.shared, 'jade_i1.csv'));
    i2 = diag_load_csv(fullfile(P.shared, 'jade_i2.csv'));
    jrand = diag_load_csv(fullfile(P.shared, 'jade_jrand.csv'));
    mask_u = diag_load_csv(fullfile(P.shared, 'jade_mask.csv'));
    n = size(X, 1);
    D = size(X, 2);
    off = zeros(n, D);
    pre = zeros(n, D);
    for i = 1:n
        pb = X(min(max(pbest_idx(i)+1, 1), n), :);
        a = X(min(max(i1(i)+1, 1), n), :);
        b = X(min(max(i2(i)+1, 1), n), :);
        trial = X(i, :) + Fs(i) * (pb - X(i, :)) + Fs(i) * (b - a);
        mask = mask_u(i, :) < cr(i);
        jr = min(max(jrand(i)+1, 1), D);
        mask(jr) = true;
        child = X(i, :);
        child(mask) = trial(mask);
        pre(i, :) = child;
        off(i, :) = min(max(child, G.lower), G.upper);
    end
    diag_write_csv(fullfile(P.out, 'test_13_jade_offspring.csv'), {'x1','x2'}, off);
    diag_write_csv(fullfile(P.out, 'test_13_jade_pre_repair.csv'), {'x1','x2'}, pre);
    fprintf('matlab test_13 done (OptMPNDS3 JADE2 one-step; not OptMPNDS)\n');
end
