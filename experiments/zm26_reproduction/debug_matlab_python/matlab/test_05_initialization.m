function test_05_initialization()
%TEST_05_INITIALIZATION  Structural stats of GLOBAL.Initialization (not seed-matched).
    P = setup_diag();
    G = ensure_global_mpdmp4(200, 100000);
    rng(1);
    Pop = G.Initialization(200);
    X = Pop.decs;
    n_out = sum(any(X < repmat(G.lower, size(X,1), 1) | X > repmat(G.upper, size(X,1), 1), 2));
    Xu = unique(X, 'rows');
    stats = [size(X,1); min(X(:,1)); max(X(:,1)); min(X(:,2)); max(X(:,2)); ...
             mean(X(:,1)); mean(X(:,2)); n_out; size(Xu,1)];
    diag_write_csv(fullfile(P.out, 'test_05_init_stats.csv'), {'field_id','value'}, [(1:numel(stats))', stats]);
    ps = G.problem.PS();
    pf = G.problem.PF();
    diag_write_csv(fullfile(P.out, 'test_05_PS.csv'), {'x1','x2'}, ps);
    diag_write_csv(fullfile(P.out, 'test_05_PF.csv'), ...
        arrayfun(@(i) sprintf('F%d', i), 1:size(pf,2), 'UniformOutput', false), pf);
    notes = {
        'OptMPNDS uses GLOBAL.Initialization = unifrnd(lower,upper).';
        'Do not compare MATLAB rng(1) coordinates to Python default_rng(1).';
        'MPDMP4.PS is the single common point (50,40); PF=CalObj(PS).';
        'getPF / PFt initialization is OptMPNDS3 only, not OptMPNDS.';
    };
    fid = fopen(fullfile(P.out, 'test_05_notes.txt'), 'w');
    for i = 1:numel(notes)
        fprintf(fid, '%s\n', notes{i});
    end
    fclose(fid);
    fprintf('matlab test_05 done\n');
end
