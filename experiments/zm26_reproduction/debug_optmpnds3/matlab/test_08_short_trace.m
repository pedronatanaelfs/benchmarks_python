function test_08_short_trace()
%TEST_08_SHORT_TRACE  5 gens from shared X0 / random arrays using MATLAB operators.
    P = setup_diag();
    G = ensure_global('MPDMP1', 20, 100000);
    X = diag_load_csv(fullfile(P.shared, 'short_X0.csv'));
    Pop = INDIVIDUAL(X);
    [Pop, FrontNo, CrowdDis] = EnvironmentalSelection(Pop, length(Pop), G.DM);
    Archive = [];
    mu_cr = 0.5; mu_f = 0.5; c = 0.05;
    rows = zeros(6, 6);
    rows(1,:) = quality_row(Pop, G, 0, 0, mu_cr, mu_f);
    diag_write_csv(fullfile(P.out, 'test_08_X_g0.csv'), {'x1','x2'}, Pop.decs);
    for g = 0:4
        cr = diag_load_csv(fullfile(P.shared, sprintf('g%d_cr.csv', g)));
        Fs = diag_load_csv(fullfile(P.shared, sprintf('g%d_F.csv', g)));
        ks = diag_load_csv(fullfile(P.shared, sprintf('g%d_pbest_k.csv', g)));
        i1 = diag_load_csv(fullfile(P.shared, sprintf('g%d_i1.csv', g)));
        i2 = diag_load_csv(fullfile(P.shared, sprintf('g%d_i2.csv', g)));
        jrand = diag_load_csv(fullfile(P.shared, sprintf('g%d_jrand.csv', g)));
        mask_u = diag_load_csv(fullfile(P.shared, sprintf('g%d_mask.csv', g)));
        N = length(Pop); D = size(Pop.decs, 2);
        Offsprings = [];
        decs = Pop.decs;
        for i = 1:N
            k = max(1, min(ks(i), max(ceil(N*0.05),1)));
            pb = getBestIndividualFromK(FrontNo, CrowdDis, k);
            Pbest = decs(pb, :);
            a = mod(i1(i), N) + 1;
            if a == i && N > 1
                a = mod(a, N) + 1;
            end
            temp = [Archive, Pop];
            nPool = length(temp);
            b = mod(i2(i), nPool) + 1;
            Parent1 = decs(a, :);
            Parent2 = temp(b).dec;
            x = decs(i, :);
            trial = x + Fs(i)*(Pbest - x) + Fs(i)*(Parent2 - Parent1);
            child = x;
            jr = mod(jrand(i), D) + 1;
            for j = 1:D
                if j == jr || mask_u(i,j) < cr(i)
                    child(j) = trial(j);
                end
            end
            Offspring = INDIVIDUAL(child, [cr(i), Fs(i)]);
            if dominated(Offspring.objs, Pop(i).objs, G.DM)
                Archive = updateArchiveLocal(Archive, Pop(i), 2*G.N);
                Offsprings = [Offsprings, Offspring];
            elseif dominated(Pop(i).objs, Offspring.objs, G.DM)
                Archive = updateArchiveLocal(Archive, Offspring, 2*G.N);
                Offsprings = [Offsprings, Pop(i)];
            else
                Offsprings = [Offsprings, Offspring, Pop(i)];
            end
        end
        oldPop = Pop;
        [Pop, FrontNo, CrowdDis] = EnvironmentalSelection(Offsprings, N, G.DM);
        discarded = setdiff(Offsprings, Pop);
        if ~isempty(discarded)
            Archive = updateArchiveLocal(Archive, discarded, 2*G.N);
        end
        tempAdd = Pop.adds(zeros(length(Pop), 2));
        S_CR = tempAdd(:,1); S_F = tempAdd(:,2);
        S_CR = S_CR(S_CR ~= 0); S_F = S_F(S_F ~= 0);
        if ~isempty(S_CR)
            mu_cr = (1-c)*mu_cr + c*mean(S_CR);
        end
        if ~isempty(S_F)
            mu_f = (1-c)*mu_f + c*(sum(S_F.^2)/sum(S_F));
        end
        rows(g+2,:) = quality_row(Pop, G, g+1, length(Archive), mu_cr, mu_f);
        diag_write_csv(fullfile(P.out, sprintf('test_08_X_g%d.csv', g+1)), {'x1','x2'}, Pop.decs);
        if ~isempty(Archive)
            diag_write_csv(fullfile(P.out, sprintf('test_08_archive_X_g%d.csv', g+1)), {'x1','x2'}, Archive.decs);
        end
    end
    diag_write_csv(fullfile(P.out, 'test_08_short_trace.csv'), ...
        {'generation','n','zm26_meanIGD','mean_dist_to_common_ps','archive_size','mu_F'}, rows);
    fprintf('matlab test_08 done\n');
end

function r = quality_row(Pop, G, gen, arch, mu_cr, mu_f)
    X = Pop.decs; F = Pop.objs;
    igd = IGD(F, G.problem.PF(), G.DM);
    ps = [50, 50];
    dist = mean(sqrt(sum((X - repmat(ps, size(X,1), 1)).^2, 2)));
    r = [gen, length(Pop), igd(1), dist, arch, mu_f];
end

function Archive = updateArchiveLocal(Archive, Population, N)
    if isempty(Population)
        return;
    end
    for i = Population
        if isempty(Archive) || length(Archive) < N
            Archive = [Archive, i];
        else
            decs = Archive.decs;
            dis = pdist2(decs, i.decs);
            [~, index] = min(dis);
            Archive(index) = i;
        end
    end
end
