function test_11_objective_grouping()
%TEST_11_OBJECTIVE_GROUPING  MPDMP4 DM ownership as used by MPNDS / envsel.
    P = setup_diag();
    G = ensure_global_mpdmp4(20, 100000);
    DM = G.DM;
    rows = zeros(numel(DM), 4);
    fid = fopen(fullfile(P.out, 'test_11_grouping.csv'), 'w');
    fprintf(fid, 'dm,matlab_columns_1based,n_obj,used_by_mpnds\n');
    for k = 1:numel(DM)
        sl = DM{k};
        fprintf(fid, '%d,%d:%d,%d,PopObj(:,DM{k})\n', k, sl(1), sl(end), numel(sl));
        rows(k, :) = [k, sl(1), sl(end), numel(sl)];
    end
    fclose(fid);
    v1 = G.problem.Map.polygons(1).Vertices;
    v2 = G.problem.Map.polygons(2).Vertices;
    % EuclideanDistance concatenates pdist2(x, Vertices) per polygon
    diag_write_csv(fullfile(P.out, 'test_11_reference_vertices_dm1.csv'), {'x','y'}, v1);
    diag_write_csv(fullfile(P.out, 'test_11_reference_vertices_dm2.csv'), {'x','y'}, v2);
    fid = fopen(fullfile(P.out, 'test_11_notes.txt'), 'w');
    fprintf(fid, 'MPDMP4 inherits MPDMP5: DM={1:3, 4:6}, M=6.\n');
    fprintf(fid, 'MPNDS/PLNDS: NDSort(PopObj(:,DM{k}), N) per party.\n');
    fprintf(fid, 'OptMPNDS EnvironmentalSelection: MPNDS then CrowdingDistance on FULL objs.\n');
    fprintf(fid, 'polygon.EuclideanDistance concatenates pdist2 to each polygon Vertices.\n');
    fclose(fid);
    fprintf('matlab test_11 done  DM1=%s  DM2=%s\n', mat2str(DM{1}), mat2str(DM{2}));
end
