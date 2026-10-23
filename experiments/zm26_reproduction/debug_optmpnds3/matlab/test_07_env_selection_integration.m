function test_07_env_selection_integration()
    P = setup_diag();
    G = ensure_global('MPDMP1', 20, 100000);
    X = diag_load_csv(fullfile(P.shared, 'envsel_X.csv'));
    Pop = INDIVIDUAL(X);
    [Pop2, FrontNo, CrowdDis] = EnvironmentalSelection(Pop, 20, G.DM);
    out = [FrontNo(:), CrowdDis(:), Pop2.decs];
    diag_write_csv(fullfile(P.out, 'test_07_env_selection.csv'), {'front','entropy','x1','x2'}, out);
    diag_write_csv(fullfile(P.out, 'test_07_selected_X.csv'), {'x1','x2'}, Pop2.decs);
    fprintf('matlab test_07 done selected=%d from %d\n', length(Pop2), length(Pop));
end
