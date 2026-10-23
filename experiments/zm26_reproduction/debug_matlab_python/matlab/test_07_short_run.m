function test_07_short_run()
%TEST_07_SHORT_RUN  5-generation OptMPNDS trace with shared parents and GA streams.
    P = setup_diag();
    N = 20;
    N_GEN = 5;
    G = ensure_global_mpdmp4(N, 100000);
    X = diag_load_csv(fullfile(P.shared, 'short_X0.csv'));
    Pop = INDIVIDUAL(X);
    [Pop, FrontNo, CrowdDis] = EnvironmentalSelection(Pop, N, G.DM);
    X = Pop.decs;
    F = Pop.objs;
    rows = zeros(N_GEN+1, 8);
    common = [50, 40];
    for g = 0:N_GEN
        rows(g+1, :) = [g, size(X,1), mean(X(:,1)), mean(X(:,2)), ...
            mean(sqrt(sum((X - repmat(common, size(X,1), 1)).^2, 2))), ...
            sum(FrontNo == 1), min(FrontNo), max(FrontNo)];
        diag_write_csv(fullfile(P.out, sprintf('test_07_X_g%d.csv', g)), {'x1','x2'}, X);
        fheader = arrayfun(@(i) sprintf('F%d', i), 1:size(F,2), 'UniformOutput', false);
        diag_write_csv(fullfile(P.out, sprintf('test_07_F_g%d.csv', g)), fheader, F);
        diag_write_csv(fullfile(P.out, sprintf('test_07_front_g%d.csv', g)), {'front'}, FrontNo(:));
        diag_write_csv(fullfile(P.out, sprintf('test_07_crowd_g%d.csv', g)), {'crowd'}, CrowdDis(:));
        if g == N_GEN
            break;
        end
        tour = diag_load_csv(fullfile(P.shared, sprintf('short_tour_g%d.csv', g)));
        parent_idx = tour(1, :) + 1; % shared file is 0-based
        parent_idx = parent_idx(1:size(X,1));
        parent_idx = max(1, min(size(X,1), parent_idx));
        diag_write_csv(fullfile(P.out, sprintf('test_07_mating_g%d.csv', g)), ...
            {'parent_index_1based'}, parent_idx(:));
        parents = X(parent_idx, :);
        mu_sbx = diag_load_csv(fullfile(P.shared, sprintf('short_ga_mu_sbx_g%d.csv', g)));
        sign01 = diag_load_csv(fullfile(P.shared, sprintf('short_ga_sign_g%d.csv', g)));
        beta_skip = diag_load_csv(fullfile(P.shared, sprintf('short_ga_beta_skip_g%d.csv', g)));
        proc = diag_load_csv(fullfile(P.shared, sprintf('short_ga_proc_g%d.csv', g)));
        site_u = diag_load_csv(fullfile(P.shared, sprintf('short_ga_site_g%d.csv', g)));
        mu_mut = diag_load_csv(fullfile(P.shared, sprintf('short_ga_mu_mut_g%d.csv', g)));
        off = ga_from_stream(parents, G.lower, G.upper, mu_sbx, sign01, ...
            beta_skip, proc, site_u, mu_mut, 1, 15, 0.5, 20);
        OffPop = INDIVIDUAL(off);
        candX = [Pop.decs; OffPop.decs];
        Combined = [Pop, OffPop];
        [Pop, FrontNo, CrowdDis] = EnvironmentalSelection(Combined, N, G.DM);
        Xs = Pop.decs;
        used = false(size(candX,1), 1);
        selected = zeros(size(Xs,1), 1);
        for i = 1:size(Xs,1)
            d = sum((candX - repmat(Xs(i,:), size(candX,1), 1)).^2, 2);
            d(used) = inf;
            [~, idx] = min(d);
            used(idx) = true;
            selected(i) = idx;
        end
        diag_write_csv(fullfile(P.out, sprintf('test_07_survived_g%d.csv', g)), ...
            {'selected_original_index'}, selected);
        X = Pop.decs;
        F = Pop.objs;
    end
    diag_write_csv(fullfile(P.out, 'test_07_trace.csv'), ...
        {'generation','n','mean_x1','mean_x2','dist_to_common_ps','n_front1','min_front','max_front'}, rows);
    fprintf('matlab test_07 done\n');
end
