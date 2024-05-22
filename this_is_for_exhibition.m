clc;clear;

% 設定參數（註解掉的部分）
% L = 0.013242
% R = 3.2645
% J = 0.01829
% B = 0.019
% Ke = 1.1895
% Kt = 1.1895
% simulation_time = 150

% 執行 Simulink 模型模擬
out = sim("PMDC_exhibition");
% out = sim("./PMDC_exhibition.slx");
% 讀取模擬輸出數據
tl = out.Tl;
f = size(tl);

% 清除舊數據
torque = 0;
y1 = 0; y2 = 0; y3 = 0; y4 = 0;

% 根據 LoadMode 處理數據（1: 斜坡負載, 2: 階梯負載）
switch LoadMode
    case 1
        % 斜坡負載模式
        i = 1;
        while 1
            if tl(i) > 0.01
                s = i;
                break
            end
            i = i + 1;
        end
        torque = out.Tl(s:f(1));
        y1 = out.omega(s:f(1));
        y2 = out.Eff(s:f(1));
        y3 = out.Pin(s:f(1));
        y4 = out.Pout(s:f(1));
    case 2
        % 階梯負載模式
        tl_pre = 0;
        j = 1;
        for i = 1:f(1)
            if tl(i) > tl_pre
                torque(j, 1) = tl(i - 1);
                y1(j, 1) = out.omega((i - 1), 1);
                y2(j, 1) = out.Eff((i - 1), 1);
                y3(j, 1) = out.Pin((i - 1), 1);
                y4(j, 1) = out.Pout((i - 1), 1);
                j = j + 1;
            end
            tl_pre = tl(i);
        end
end

% 繪圖
fig = figure('Visible', 'off');
clf;

% 創建具有4個y軸的空坐標系統
h = myaxisc(4, 0.10, [0.1, 0.1, 0.8, 0.8]);

% 根據 PlotMode 繪製數據
switch PlotMode
    case 1
        p(1) = plot(h.p(1), torque, y1, 'b', 'LineWidth', 1.2);
        p(2) = plot(h.p(2), torque, y2, 'Color', [0.4660 0.6740 0.1880], 'LineWidth', 1.2);
        p(3) = plot(h.p(3), torque, y3, 'r', 'LineWidth', 1.2);
        p(4) = plot(h.p(4), torque, y4, 'Color', [0.9290 0.6940 0.1250], 'LineWidth', 1.2);
        print("case1");
    case 2
        p(1) = plot(h.p(1), torque, y1, 'b-*', 'LineWidth', 1.1);
        p(2) = plot(h.p(2), torque, y2, '-*', 'Color', [0.4660 0.6740 0.1880], 'LineWidth', 1.1);
        p(3) = plot(h.p(3), torque, y3, 'r-*', 'LineWidth', 1.1);
        p(4) = plot(h.p(4), torque, y4, '-*', 'Color', [0.9290 0.6940 0.1250], 'LineWidth', 1.1);
        print("case2");
end

% 自動縮放 Y 軸
h.autoscale

% 修改外觀和縮放
h.autoy(3)
l = size(torque);
h.xlim([0, torque(l(1), 1) + 0.05]);
h.ylim(2, [0, 100]);

% 啟用網格
h.gridon

% 修改 y 軸顏色
h.ycolor(1, 'b');
h.ycolor(2, [0.4660 0.6740 0.1880]);
h.ycolor(3, 'r');
h.ycolor(4, [0.9290 0.6940 0.1250]);

% 添加 y 軸標籤
h.ylabel(1, 'Speed (RPM)');
h.ylabel(2, 'Efficiency (%)');
h.ylabel(3, 'Pin (W)');
h.ylabel(4, 'Pout (W)');

% 添加 x 軸標籤
h.xlabel('TL (Nm)');

% 更改整個 myaxisc 對象的位置
h.position([0.1, 0.1, 0.8, 0.8], 0.12);

% 更改所有字體大小
h.fontsize(10)

% 儲存圖形並關閉
print('-dpng', '-r300', './static/output_figure.png');
close(fig);
