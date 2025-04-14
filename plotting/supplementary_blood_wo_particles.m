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

times = zeros(1,1000);
data = zeros(1,1000);

%%% load the evaluation data %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%% load results data
result_file_name = './../data/plotting/no_particles_avg.csv';
if exist(result_file_name, 'file')
    result_data = readmatrix(result_file_name);
    offset = result_data(1,2)
    times = result_data(:,1);
    data = result_data(:,2) - offset;
end

%% plot frequency shift for moving blood
figure;
hold on;
plot(times(1:200,1),data(501:700,1), '-', 'Color', colors{2},'LineWidth',2.5)
xline(0.25,':',{'Background flow pump','turned on'},'LineWidth',2.5,'Interpreter',"latex",'FontSize',legendfontsize);
box off
axis tight
xaxisproperties= get(gca, 'XAxis');
xaxisproperties.TickLabelInterpreter = 'latex'; % latex for x-axis
yaxisproperties= get(gca, 'YAxis');
yaxisproperties.TickLabelInterpreter = 'latex'; % latex for y-axis
%ylim(y_bounds)
set(gca, 'YGrid', 'on', 'XGrid', 'on')
set(gca,'linewidth',2)
%set(gca, 'YScale', 'log');
set(gca,'FontSize',fontsize);
xlabel('Time [s]','interpreter','latex');
ylabel('Frequency Shift [Hz]','interpreter','latex');
legend({['Blood without SPIONs']},...
    'Location','northeast','NumColumns',1,'Interpreter',"latex",'FontSize',legendfontsize)
legend boxoff;
file_name = strcat('suppl_blood_no_particles');
saveas(gcf,file_name,'epsc')
saveas(gcf,file_name,'png')
