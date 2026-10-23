function test_02_initial_population_quality()
%TEST_02  Copy gen-0 quality from test_01 meta into one table.
    P = setup_diag();
    names = {'MPDMP1', 'MPDMP4'};
    paper = [0.0447, 0.0133];
    rows = zeros(2, 8);
    for t = 1:2
        meta = diag_load_csv_header(fullfile(P.out, [lower(names{t}) '_init_meta.csv']));
        rows(t,:) = [t, meta(1), meta(2), meta(4), meta(5), meta(6), paper(t), meta(5)/paper(t)];
    end
    diag_write_csv(fullfile(P.out, 'test_02_initial_population_quality.csv'), ...
        {'problem_id','n_pf1','n_pf2','n_after_envsel','zm26_meanIGD','mean_dist_to_common_ps','paper_final_zm26','init_vs_paper_ratio'}, rows);
    fprintf('matlab test_02 done\n');
end

function A = diag_load_csv_header(path)
    A = dlmread(path, ',', 1, 0);
    if size(A,1) > 1
        A = A(end,:);
    end
end
