function test_05_f_cr_adaptation()
    P = setup_diag();
    c = 0.05;
    mu_cr = 0.5; mu_f = 0.5;
    rows = zeros(5, 8);
    for g = 0:4
        cr = diag_load_csv(fullfile(P.shared, sprintf('g%d_cr.csv', g)));
        Fs = diag_load_csv(fullfile(P.shared, sprintf('g%d_F.csv', g)));
        s_cr = cr(cr ~= 0);
        s_f = Fs(Fs ~= 0);
        mu_cr_b = mu_cr; mu_f_b = mu_f;
        if ~isempty(s_cr)
            mu_cr = (1-c)*mu_cr + c*mean(s_cr);
        end
        if ~isempty(s_f)
            mu_f = (1-c)*mu_f + c*(sum(s_f.^2)/sum(s_f));
        end
        rows(g+1,:) = [g, mu_cr_b, mu_f_b, mean(cr), mean(Fs), mu_cr, mu_f, numel(s_cr)];
    end
    diag_write_csv(fullfile(P.out, 'test_05_f_cr_adaptation.csv'), ...
        {'generation','mu_CR_before','mu_F_before','sampled_CR_mean','sampled_F_mean','mu_CR_after','mu_F_after','n_S_CR'}, rows);
    fprintf('matlab test_05 done\n');
end
