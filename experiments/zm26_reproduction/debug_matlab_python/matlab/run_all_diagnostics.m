function run_all_diagnostics(includeNative)
%RUN_ALL_DIAGNOSTICS  Master MATLAB script for the MPDMP4 / OptMPNDS audit.
%
% Usage (from MATLAB):
%   cd '<repo>/experiments/zm26_reproduction/debug_matlab_python/matlab'
%   run_all_diagnostics
%
% Optional slow native 5-run sanity (N=200, FE=80000):
%   run_all_diagnostics(true)
%
% Prerequisites:
%   1. Python diagnostics already generated shared_inputs/
%   2. MATLAB R2017b+ (polyshape / nsidedpoly)
%   3. Statistics Toolbox (pdist2 in polygon.EuclideanDistance)
%
% Outputs: ../matlab_outputs/*.csv
% Then return the matlab_outputs/ folder to Python compare_outputs.py.

    if nargin < 1
        includeNative = false;
    end
    P = setup_diag();
    fprintf('diag root: %s\n', P.diagRoot);
    fprintf('She src:   %s\n', P.she);
    fprintf('shared:    %s\n', P.shared);
    fprintf('output:    %s\n', P.out);

    tests = {@test_01_problem, @test_02_mpn_sorting, @test_03_crowding, ...
             @test_04_environmental_selection, @test_05_initialization, ...
             @test_06_variation, @test_07_short_run, @test_08_unique_rows, ...
             @test_09_one_by_one, @test_10_boundary, @test_11_objective_grouping, ...
             @test_13_jade2};
    for i = 1:numel(tests)
        fprintf('\n===== %s =====\n', func2str(tests{i}));
        feval(tests{i});
    end
    if includeNative
        fprintf('\n===== test_12_native_runs =====\n');
        test_12_native_runs();
    else
        fprintf('\nSkipped test_12 native 5-run (slow). To run later:\n');
        fprintf('  test_12_native_runs\n');
        fprintf('or:\n');
        fprintf('  run_all_diagnostics(true)\n');
    end
    fprintf('\nPASS/finished: MATLAB diagnostics written to\n  %s\n', P.out);
    fprintf('Copy this folder back into the repo (if you ran MATLAB elsewhere),\n');
    fprintf('then from the diagnostic directory run:\n');
    fprintf('  python compare_outputs.py\n');
end
