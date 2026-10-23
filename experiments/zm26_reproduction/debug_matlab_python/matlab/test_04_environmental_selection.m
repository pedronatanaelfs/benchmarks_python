function test_04_environmental_selection()
%TEST_04_ENVIRONMENTAL_SELECTION  OptMPNDS EnvironmentalSelection on 200 candidates.
    P = setup_diag();
    N = 100;
    G = ensure_global_mpdmp4(N, 100000);
    X = diag_load_csv(fullfile(P.shared, 'envsel_X.csv'));
    Pop = INDIVIDUAL(X);
    objs = Pop.objs;
    [FrontAll, MaxFNo] = MPNDS(objs, Pop.cons, N, G.DM);
    CrowdAll = CrowdingDistance(objs, FrontAll);
    survived = zeros(size(X,1), 1);

    [NewPop, FrontNo, CrowdDis] = EnvironmentalSelection(Pop, N, G.DM);
    Xs = NewPop.decs;
    selected = zeros(size(Xs,1), 1);
    used = false(size(X,1), 1);
    for i = 1:size(Xs,1)
        d = sum((X - repmat(Xs(i,:), size(X,1), 1)).^2, 2);
        d(used) = inf;
        [~, idx] = min(d);
        used(idx) = true;
        selected(i) = idx;
    end
    survived(used) = 1;

    cand = [(1:size(X,1))', FrontAll(:), CrowdAll(:), survived];
    diag_write_csv(fullfile(P.out, 'test_04_candidates.csv'), ...
        {'original_index','front','crowding','survived'}, cand);
    sel = [selected, FrontNo(:), CrowdDis(:)];
    diag_write_csv(fullfile(P.out, 'test_04_selected.csv'), ...
        {'selected_original_index','front','crowding'}, sel);
    diag_write_csv(fullfile(P.out, 'test_04_meta.csv'), {'field_id','value'}, ...
        [(1:4)', [size(X,1); N; MaxFNo; size(Xs,1)]]);
    diag_write_csv(fullfile(P.out, 'test_04_selected_X.csv'), {'x1','x2'}, Xs);
    fprintf('matlab test_04 done  selected=%d  max_fno=%g\n', size(Xs,1), MaxFNo);
end
