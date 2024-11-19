package org.jeongkkili.bombom.speaker.domain;

import org.jeongkkili.bombom.senior.domain.Senior;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.OneToOne;
import jakarta.persistence.Table;
import lombok.AccessLevel;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;

@Getter
@Entity
@Table(name = "speaker")
@NoArgsConstructor(access = AccessLevel.PROTECTED)
public class Speaker {

	@Id
	@GeneratedValue(strategy = GenerationType.IDENTITY)
	@Column(name = "speaker_id")
	private Long id;

	@OneToOne
	@JoinColumn(name = "senior_id")
	private Senior senior;

	@Column(name = "serial_num", nullable = false, unique = true)
	private String serialNum;

	@Builder
	public Speaker(Senior senior, String serialNum) {
		this.senior = senior;
		this.serialNum = serialNum;
	}
}
