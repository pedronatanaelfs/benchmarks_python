function test_12_native_runs()
%TEST_12_NATIVE_RUNS  5 native stochastic OptMPNDS runs on MPDMP4 (slow).
% N=200, evaluation=80000. Independent RNG; do not compare populations exactly.
% Opens one figure per run (GLOBAL.NotTermination calls problem.Draw).
    P = setup_diag();
    nRuns = 5;
    N = 200;
    FE = 80000;
    rows = zeros(nRuns, 9);
    for r = 1:nRuns
        fprintf('matlab native run %d/%d ...\n', r, nRuns);
        rng(r);
        G = GLOBAL('-algorithm', @OptMPNDS, '-problem', @MPDMP4, ...
                   '-N', N, '-evaluation', FE, '-save', 1, '-run', r);
        t0 = tic;
        G.Start();
        rt = toc(t0);
        Pop = G.result{end};
        X = Pop.decs;
        F = Pop.objs;
        igd_she = IGD(F, G.PF, G.DM);
        dist = mean(sqrt(sum((X - repmat([50,40], size(X,1), 1)).^2, 2)));
        rows(r, :) = [r, r, igd_she(1), dist, mean(X(:,1)), mean(X(:,2)), ...
                      std(X(:,1)), std(X(:,2)), rt];
        diag_write_csv(fullfile(P.out, sprintf('test_12_X_run%d.csv', r)), {'x1','x2'}, X);
        fprintf('  SheIGD=%.6g  meanDistToPS=%.4g  t=%.1fs\n', igd_she(1), dist, rt);
    end
    diag_write_csv(fullfile(P.out, 'test_12_native_runs.csv'), ...
        {'run','seed','she_IGD','mean_dist_to_common_ps','pop_mean_x1','pop_mean_x2','pop_std_x1','pop_std_x2','runtime_sec'}, rows);
    fprintf('matlab test_12 done\n');
end
