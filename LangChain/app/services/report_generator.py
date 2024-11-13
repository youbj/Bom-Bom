from fpdf import FPDF
from datetime import datetime, timedelta
from typing import List, Dict
import logging
import json
from statistics import mean
import matplotlib.pyplot as plt
import io
import os

logger = logging.getLogger(__name__)

class ReportGenerator:
    def __init__(self):
        self.reports_dir = "data/reports"
        os.makedirs(self.reports_dir, exist_ok=True)

    def generate_pdf_report(self, conversation_data: List[Dict], start_date: datetime, end_date: datetime) -> str:
        """PDF 보고서 생성"""
        try:
            pdf = FPDF()
            pdf.add_page()
            
            # 보고서 제목
            pdf.set_font("Arial", "B", 16)
            pdf.cell(0, 10, f"노인 케어 보고서", ln=True, align='C')
            pdf.cell(0, 10, f"기간: {start_date.strftime('%Y-%m-%d')} - {end_date.strftime('%Y-%m-%d')}", ln=True, align='C')
            
            # 대화 통계
            self._add_conversation_stats(pdf, conversation_data)
            
            # 감정 상태 추이
            self._add_emotional_trend(pdf, conversation_data)
            
            # 건강 상태 요약
            self._add_health_summary(pdf, conversation_data)
            
            # 위험 요소
            self._add_risk_factors(pdf, conversation_data)
            
            # 키워드 분석
            self._add_keyword_analysis(pdf, conversation_data)
            
            # 권장 조치사항
            self._add_recommendations(pdf, conversation_data)
            
            # 파일 저장
            output_path = os.path.join(
                self.reports_dir,
                f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            )
            pdf.output(output_path)
            return output_path
            
        except Exception as e:
            logger.error(f"Failed to generate report: {str(e)}")
            raise

    def _add_conversation_stats(self, pdf: FPDF, conversation_data: List[Dict]):
        """대화 통계 추가"""
        pdf.add_page()
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, "대화 통계", ln=True)
        
        pdf.set_font("Arial", "", 12)
        total_messages = len(conversation_data)
        user_messages = sum(1 for msg in conversation_data if msg['speaker_type'] == 'USER')
        
        stats = [
            f"총 대화 수: {total_messages}",
            f"사용자 메시지: {user_messages}",
            f"AI 응답: {total_messages - user_messages}",
            f"평균 메시지 길이: {sum(len(msg['text_content']) for msg in conversation_data) / total_messages:.1f}자"
        ]
        
        for stat in stats:
            pdf.cell(0, 10, stat, ln=True)

    def _add_emotional_trend(self, pdf: FPDF, conversation_data: List[Dict]):
        """감정 상태 추이 차트 추가"""
        pdf.add_page()
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, "감정 상태 추이", ln=True)
        
        # 감정 점수 추출
        sentiment_data = [
            {
                'date': msg['created_at'],
                'score': msg.get('sentiment_analysis', {}).get('score', 50)
            }
            for msg in conversation_data
            if msg['speaker_type'] == 'USER'
        ]
        
        if sentiment_data:
            # matplotlib로 그래프 생성
            plt.figure(figsize=(10, 6))
            plt.plot(
                [d['date'] for d in sentiment_data],
                [d['score'] for d in sentiment_data],
                marker='o'
            )
            plt.title("감정 상태 변화")
            plt.xlabel("날짜")
            plt.ylabel("감정 점수")
            plt.grid(True)
            
            # 그래프를 이미지로 저장
            img_buffer = io.BytesIO()
            plt.savefig(img_buffer, format='png')
            img_buffer.seek(0)
            
            # PDF에 이미지 추가
            pdf.image(img_buffer, x=10, y=None, w=190)
            plt.close()

    def _add_health_summary(self, pdf: FPDF, conversation_data: List[Dict]):
        """건강 상태 요약 추가"""
        pdf.add_page()
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, "건강 상태 요약", ln=True)
        
        # 건강 지표 수집
        health_data = [
            msg.get('health_monitoring', {})
            for msg in conversation_data
            if msg.get('health_monitoring')
        ]
        
        if health_data:
            pdf.set_font("Arial", "", 12)
            
            # 각 건강 지표의 평균 계산
            avg_scores = {
                'physical': mean([d.get('physical_health_score', 0) for d in health_data if d.get('physical_health_score') is not None]),
                'mental': mean([d.get('mental_health_score', 0) for d in health_data if d.get('mental_health_score') is not None]),
                'sleep': mean([d.get('sleep_quality_score', 0) for d in health_data if d.get('sleep_quality_score') is not None]),
                'appetite': mean([d.get('appetite_level_score', 0) for d in health_data if d.get('appetite_level_score') is not None])
            }
            
            for category, score in avg_scores.items():
                pdf.cell(0, 10, f"{category.capitalize()}: {score:.1f}/100", ln=True)

    def _add_risk_factors(self, pdf: FPDF, conversation_data: List[Dict]):
        """위험 요소 섹션 추가"""
        pdf.add_page()
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, "위험 요소 분석", ln=True)
        
        # 위험 평가 데이터 수집
        risk_data = [
            msg.get('risk_assessment', {})
            for msg in conversation_data
            if msg.get('risk_assessment')
        ]
        
        if risk_data:
            pdf.set_font("Arial", "", 12)
            
            # 위험 수준별 카운트
            risk_counts = {
                'HIGH': sum(1 for d in risk_data if d.get('risk_level') == 'HIGH'),
                'MEDIUM': sum(1 for d in risk_data if d.get('risk_level') == 'MEDIUM'),
                'LOW': sum(1 for d in risk_data if d.get('risk_level') == 'LOW')
            }
            
            for level, count in risk_counts.items():
                pdf.cell(0, 10, f"{level} 위험 발생: {count}회", ln=True)
            
            # 주요 위험 요인 집계
            risk_factors = {}
            for d in risk_data:
                for factor in d.get('risk_factors', []):
                    risk_factors[factor] = risk_factors.get(factor, 0) + 1
            
            if risk_factors:
                pdf.cell(0, 10, "\n주요 위험 요인:", ln=True)
                for factor, count in sorted(risk_factors.items(), key=lambda x: x[1], reverse=True):
                    pdf.cell(0, 10, f"- {factor}: {count}회", ln=True)

    def _add_keyword_analysis(self, pdf: FPDF, conversation_data: List[Dict]):
        """키워드 분석 추가"""
        pdf.add_page()
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, "주요 키워드 분석", ln=True)
        
        # 키워드 빈도 집계
        keywords = {}
        for msg in conversation_data:
            for keyword in msg.get('keywords', []):
                keywords[keyword] = keywords.get(keyword, 0) + 1
        
        if keywords:
            pdf.set_font("Arial", "", 12)
            for keyword, count in sorted(keywords.items(), key=lambda x: x[1], reverse=True)[:10]:
                pdf.cell(0, 10, f"- {keyword}: {count}회", ln=True)

    def _add_recommendations(self, pdf: FPDF, conversation_data: List[Dict]):
        """권장 조치사항 추가"""
        pdf.add_page()
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, "권장 조치사항", ln=True)
        
        # 위험 평가에서 필요 조치사항 수집
        needed_actions = set()
        for msg in conversation_data:
            if msg.get('risk_assessment'):
                needed_actions.update(msg['risk_assessment'].get('needed_actions', []))
        
        if needed_actions:
            pdf.set_font("Arial", "", 12)
            for action in sorted(needed_actions):
                pdf.cell(0, 10, f"- {action}", ln=True)