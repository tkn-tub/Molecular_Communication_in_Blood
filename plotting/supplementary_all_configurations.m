%%% workspace %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

clc;
clear all;
close all;

addpath('./../data/plotting/');

%% Figures

paper_figs = true;

% plot layout
fontsize=20;%fontsize value
legendfontsize=17;%fontsize value
set(groot,'defaultfigureposition',[400, 250, 1000, 400])
colors = {'#b00c1c','#f34859','#f88e99','#fab7be','#6f4688','#a078b9','#bea3cf','#d4c2df','#145c84','#1e8fcc','#5db6e7','#96d0f0'};
lines = {'-diamond','-o','-s','-*'};
y_bounds = [-5,38]

%%% create evaluation collection structures %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

exp_type = ["blood", "glyc", "water"];
exp_inj = ["90degree","0degree"];
exp_dist = ["5cm","10cm","15cm","20cm"];
exp_velo = ["7,5cms","15cms"];

max_type = size(exp_type,2);
max_inj = size(exp_inj,2);
max_dist = size(exp_dist,2);
max_velo = size(exp_velo,2);
max_entries = 299;

times = zeros(max_type,max_inj,max_dist,max_velo,max_entries);
data = zeros(max_type,max_inj,max_dist,max_velo,max_entries);
theory = zeros(max_type,max_inj,max_dist,max_velo,max_entries);


%%% load the evaluation data %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%% load results data
P = '.././data/plotting/';

for t = 1:max_type
    for i = 1:max_inj
        for d = 1:max_dist
            for v = 1:max_velo
                result_file_name = strcat(P,exp_type(t),'_',exp_inj(i),'_',exp_dist(d),'_',exp_velo(v),'.csv');
                if exist(result_file_name, 'file')
                    result_data = readmatrix(result_file_name);
                    times(t,i,d,v,:) = result_data(:,1);
                    data(t,i,d,v,:) = result_data(:,2);
                    theory(t,i,d,v,:) = result_data(:,3);
                end
            end
        end
    end
end

%% plot every SIR for medium, injection, velocity over changing distance

time_points = zeros(max_entries,1);
data_points = zeros(max_entries,1);
theory_points = zeros(max_entries,1);
for t = 1:max_type
    for i = 1:max_inj
        for v = 1:max_velo
            figure;
            hold on;
            for d = 1:max_dist
                c_idx = (t - 1) * max_dist + d;
                l_str = exp_dist(d);
                time_points(:,1) = times(t,i,d,v,:);
                data_points(:,1) = data(t,i,d,v,:);
                theory_points(:,1) = theory(t,i,d,v,:);
                plot(time_points(:,1),data_points(:,1), lines{d}, 'Color', colors{c_idx}, ...
                    'DisplayName', strcat(l_str, ' data') ,'LineWidth',2.5, ...
                    'MarkerIndices',1:20:length(data_points),'MarkerSize',10)
                %plot(time_points(:,1),theory_points(:,1), ':', 'Color', colors{c_idx}, 'DisplayName', strcat(l_str, ' theory') ,'LineWidth',2.5)
            end
            box off
            axis tight
            xaxisproperties= get(gca, 'XAxis');
            xaxisproperties.TickLabelInterpreter = 'latex'; % latex for x-axis
            yaxisproperties= get(gca, 'YAxis');
            yaxisproperties.TickLabelInterpreter = 'latex'; % latex for y-axis
            ylim(y_bounds)
            set(gca, 'YGrid', 'on', 'XGrid', 'on')
            set(gca,'linewidth',2)
            %set(gca, 'YScale', 'log');
            set(gca,'FontSize',fontsize);
            xlabel('Time [s]','interpreter','latex');
            ylabel('Frequency Shift [Hz]','interpreter','latex');
            legend({['$d = 5 \:\mathrm{cm}$'], ['$d = 10 \:\mathrm{cm}$'], ...
                ['$d = 15 \:\mathrm{cm}$'], ['$d = 20 \:\mathrm{cm}$']},...
                'Location','northeast','NumColumns',2,'Interpreter',"latex",'FontSize',legendfontsize)
            legend boxoff;
            file_name = strcat('suppl_',exp_type(t),'_',exp_velo(v),'_', exp_inj(i));
            saveas(gcf,file_name,'epsc')
            saveas(gcf,file_name,'png')
            hold off;
        end
    end
end

