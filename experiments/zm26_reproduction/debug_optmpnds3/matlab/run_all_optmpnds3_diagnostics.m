function run_all_optmpnds3_diagnostics(includeNative)
%RUN_ALL_OPTMPNDS3_DIAGNOSTICS
%
%   cd '<repo>/experiments/zm26_reproduction/debug_optmpnds3/matlab'
%   run_all_optmpnds3_diagnostics
%
% Optional native 5-run (N=200, FE=80000, MPDMP1):
%   run_all_optmpnds3_diagnostics(true)

    if nargin < 1
        includeNative = false;
    end
    P = setup_diag();
    fprintf('diag root: %s\n', P.diagRoot);
    fprintf('She src:   %s\n', P.she);
    fprintf('shared:    %s\n', P.shared);
    fprintf('output:    %s\n', P.out);

    tests = {@test_04_pbest_selection, @test_05_f_cr_adaptation, ...
             @test_06_archive_update, @test_07_env_selection_integration, ...
             @test_08_short_trace, @test_03_archive_initialization, ...
             @test_01_pft_initialization, @test_02_initial_population_quality};
    for i = 1:numel(tests)
        fprintf('\n===== %s =====\n', func2str(tests{i}));
        feval(tests{i});
    end
    if includeNative
        fprintf('\n===== test_09_native_5run =====\n');
        test_09_native_5run();
    else
        fprintf('\nSkipped test_09 native 5-run. Later: test_09_native_5run\n');
    end
    fprintf('\nMATLAB outputs: %s\n', P.out);
    fprintf('Then: python compare_optmpnds3_outputs.py\n');
end
