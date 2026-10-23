function test_09_native_5run()
%TEST_09  5 native OptMPNDS3 runs on MPDMP1 (slow). Independent RNG.
    P = setup_diag();
    nRuns = 5; N = 200; FE = 80000;
    rows = zeros(nRuns, 7);
    for r = 1:nRuns
        fprintf('matlab native OptMPNDS3 MPDMP1 %d/%d ...\n', r, nRuns);
        rng(r);
        G = GLOBAL('-algorithm', @OptMPNDS3, '-problem', @MPDMP1, ...
                   '-N', N, '-evaluation', FE, '-save', 1, '-run', r);
        t0 = tic;
        G.Start();
        rt = toc(t0);
        Pop = G.result{end};
        X = Pop.decs; F = Pop.objs;
        igd = IGD(F, G.PF, G.DM);
        dist = mean(sqrt(sum((X - repmat([50,50], size(X,1), 1)).^2, 2)));
        rows(r,:) = [r, r, igd(1), dist, mean(X(:,1)), mean(X(:,2)), rt];
        diag_write_csv(fullfile(P.out, sprintf('test_09_X_run%d.csv', r)), {'x1','x2'}, X);
        fprintf('  sheIGD=%.4g dist=%.3g t=%.1fs\n', igd(1), dist, rt);
    end
    diag_write_csv(fullfile(P.out, 'test_09_native_5run.csv'), ...
        {'run','seed','zm26_meanIGD','mean_dist_to_common_ps','pop_mean_x1','pop_mean_x2','runtime_sec'}, rows);
    fprintf('matlab test_09 done\n');
end
