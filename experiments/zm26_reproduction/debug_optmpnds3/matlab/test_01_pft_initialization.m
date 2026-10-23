function test_01_pft_initialization()
%TEST_01_PFT_INITIALIZATION  Native getPF for MPDMP1 and MPDMP4 (slow, ~20000 FE each).
    P = setup_diag();
    names = {'MPDMP1', 'MPDMP4'};
    ps = [50 50; 50 40];
    for t = 1:numel(names)
        fprintf('getPF %s ...\n', names{t});
        rng(1);
        G = ensure_global(names{t}, 200, 100000);
        t0 = tic;
        [PF1, PF2] = getPF(G);
        rt = toc(t0);
        X1 = PF1.decs; X2 = PF2.decs;
        Pop = [PF1, PF2];
        n_concat = length(Pop);
        [Pop2, FrontNo, CrowdDis] = EnvironmentalSelection(Pop, length(Pop), G.DM);
        X = Pop2.decs; F = Pop2.objs;
        igd = IGD(F, G.problem.PF(), G.DM);
        dist = sqrt(sum((X - repmat(ps(t,:), size(X,1), 1)).^2, 2));
        meta = [length(PF1), length(PF2), n_concat, length(Pop2), igd(1), ...
                mean(dist), min(dist), mean(X(:,1)), mean(X(:,2)), rt];
        stem = lower(names{t});
        diag_write_csv(fullfile(P.out, [stem '_pf1_X.csv']), {'x1','x2'}, X1);
        diag_write_csv(fullfile(P.out, [stem '_pf2_X.csv']), {'x1','x2'}, X2);
        diag_write_csv(fullfile(P.out, [stem '_init_X.csv']), {'x1','x2'}, X);
        diag_write_csv(fullfile(P.out, [stem '_init_F.csv']), arrayfun(@(i) sprintf('f%d', i), 1:size(F,2), 'UniformOutput', false), F);
        diag_write_csv(fullfile(P.out, [stem '_init_meta.csv']), ...
            {'n_pf1','n_pf2','n_concat','n_after_envsel','zm26_meanIGD','mean_dist_to_common_ps','min_dist_to_common_ps','pop_mean_x1','pop_mean_x2','runtime_sec'}, meta);
        fprintf('  |PF1|=%d |PF2|=%d n=%d sheIGD=%.4g meanDist=%.3g t=%.1fs\n', ...
            length(PF1), length(PF2), length(Pop2), igd(1), mean(dist), rt);
    end
    fprintf('matlab test_01 done\n');
end
