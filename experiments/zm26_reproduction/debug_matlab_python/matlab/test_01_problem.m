function test_01_problem()
%TEST_01_PROBLEM  MPDMP4 CalObj sanity check on shared X.
    P = setup_diag();
    G = ensure_global_mpdmp4(20, 100000);
    X = diag_load_csv(fullfile(P.shared, 'mpdmp4_X.csv'));
    F = G.problem.CalObj(X);
    data = [X, F];
    header = [{'x1','x2'}, arrayfun(@(i) sprintf('F%d', i), 1:size(F,2), 'UniformOutput', false)];
    diag_write_csv(fullfile(P.out, 'test_01_problem.csv'), header, data);

    DM = G.DM;
    meta_fields = {'n_var'; 'n_obj'; 'n_dm'; 'xl0'; 'xl1'; 'xu0'; 'xu1'; ...
                   'n_obj_dm1'; 'n_obj_dm2'; 'slice_dm1_start'; 'slice_dm1_stop'; ...
                   'slice_dm2_start'; 'slice_dm2_stop'};
    sl1 = DM{1}; sl2 = DM{2};
    meta_vals = [G.D; G.M; numel(DM); G.lower(1); G.lower(2); G.upper(1); G.upper(2); ...
                 numel(sl1); numel(sl2); sl1(1); sl1(end)+1; sl2(1); sl2(end)+1];
    % 0-based slice start/stop to match Python slice.start / slice.stop
    meta_vals(10:13) = [sl1(1)-1; sl1(end); sl2(1)-1; sl2(end)];
    diag_write_csv(fullfile(P.out, 'test_01_meta.csv'), {'field_id','value'}, [(1:numel(meta_vals))', meta_vals]);
    fid = fopen(fullfile(P.out, 'test_01_meta_fields.csv'), 'w');
    fprintf(fid, 'field\n');
    for i = 1:numel(meta_fields)
        fprintf(fid, '%s\n', meta_fields{i});
    end
    fclose(fid);

    ps = G.problem.PS();
    pf = G.problem.PF();
    diag_write_csv(fullfile(P.out, 'test_01_matlab_PS.csv'), {'x1','x2'}, ps);
    diag_write_csv(fullfile(P.out, 'test_01_matlab_PF.csv'), ...
        arrayfun(@(i) sprintf('F%d', i), 1:size(pf,2), 'UniformOutput', false), pf);

    % Polygon vertices (DM ownership of EuclideanDistance = pdist2 to Vertices)
    v1 = G.problem.Map.polygons(1).Vertices;
    v2 = G.problem.Map.polygons(2).Vertices;
    diag_write_csv(fullfile(P.out, 'test_01_vertices_dm1.csv'), {'x','y'}, v1);
    diag_write_csv(fullfile(P.out, 'test_01_vertices_dm2.csv'), {'x','y'}, v2);
    fprintf('matlab test_01 done  F=%dx%d\n', size(F,1), size(F,2));
end
