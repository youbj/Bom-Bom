import torch
import torch.nn as nn
import torch.optim as optim

# 모델 정의
class BiLSTMModel(nn.Module):
    def __init__(self):
        super(BiLSTMModel, self).__init__()
        self.lstm1 = nn.LSTM(input_size=52, hidden_size=50, num_layers=1, bidirectional=True, batch_first=True)
        self.lstm2 = nn.LSTM(input_size=100, hidden_size=50, num_layers=1, bidirectional=True, batch_first=True)
        self.dropout = nn.Dropout(0.5)  # Dropout 비율 증가
        self.flatten = nn.Flatten()
        self.fc1 = nn.Linear(50 * 2, 50)  # `fc1` 출력 차원과 `fc2` 입력 차원을 일치시킴
        self.fc2 = nn.Linear(50, 4)       # 최종 출력 차원을 4로 설정 (클래스 수)

    def forward(self, x):
        x, _ = self.lstm1(x)
        x, _ = self.lstm2(x)
        x = self.dropout(x)
        x = x[:, -1, :]  # 마지막 타임스텝의 출력값 사용
        x = self.fc1(x)
        x = torch.relu(x)
        x = self.fc2(x)
        return x
# 모델 인스턴스 생성
model = BiLSTMModel()
print(model)
